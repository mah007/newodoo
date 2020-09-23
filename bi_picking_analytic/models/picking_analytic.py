# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api,_
from datetime import datetime
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero, float_compare


class StockMove(models.Model):
	_inherit = "stock.move"

	analytic_account_id = fields.Many2one('account.analytic.account',
		string='Analytic Account')
	tag_ids  = fields.Many2many('account.analytic.tag', string= 'Tag')
	
	def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
		"""
		Generate the account.move.line values to post to track the stock valuation difference due to the
		processing of the given quant.
		"""
		self.ensure_one()
		if self._context.get('force_valuation_amount'):
			valuation_amount = self._context.get('force_valuation_amount')
		else:
			valuation_amount = cost

		# the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
		# the company currency... so we need to use round() before creating the accounting entries.
		debit_value = self.company_id.currency_id.round(valuation_amount)

		# check that all data is correct
		if self.company_id.currency_id.is_zero(debit_value):
			raise UserError(_("The cost of %s is currently equal to 0. Change the cost or the configuration of your product to avoid an incorrect valuation.") % (self.product_id.name,))
		credit_value = debit_value
		# if self.company_id.anglo_saxon_accounting == False:
		if self.product_id.cost_method == 'average' and self.company_id.anglo_saxon_accounting:
			# in case of a supplier return in anglo saxon mode, for products in average costing method, the stock_input
			# account books the real purchase price, while the stock account books the average price. The difference is
			# booked in the dedicated price difference account.
			if self.location_dest_id.usage == 'supplier' and self.origin_returned_move_id and self.origin_returned_move_id.purchase_line_id:
				debit_value = self.origin_returned_move_id.price_unit * qty
			# in case of a customer return in anglo saxon mode, for products in average costing method, the stock valuation
			# is made using the original average price to negate the delivery effect.
			if self.location_id.usage == 'customer' and self.origin_returned_move_id:
				debit_value = self.origin_returned_move_id.price_unit * qty
				credit_value = debit_value
		partner_id = (self.picking_id.partner_id and self.env['res.partner']._find_accounting_partner(self.picking_id.partner_id).id) or False
		debit_line_vals = {
			'name': self.name,
			'product_id': self.product_id.id,
			'quantity': qty,
			'product_uom_id': self.product_id.uom_id.id,
			'ref': self.picking_id.name,
			'partner_id': partner_id,
			'debit': debit_value if debit_value > 0 else 0,
			'credit': -debit_value if debit_value < 0 else 0,
			'account_id': debit_account_id,
		}
		credit_line_vals = {
			'name': self.name,
			'product_id': self.product_id.id,
			'quantity': qty,
			'product_uom_id': self.product_id.uom_id.id,
			'ref': self.picking_id.name,
			'partner_id': partner_id,
			'credit': credit_value if credit_value > 0 else 0,
			'debit': -credit_value if credit_value < 0 else 0,
			'account_id': credit_account_id,

		}

		if self.picking_type_id.code == 'outgoing' and self.analytic_account_id.id:
			debit_line_vals.update({'analytic_account_id':self.analytic_account_id.id})


		if self.picking_type_id.code == 'outgoing':
			if self.picking_type_id.account_id:
				debit_line_vals.update({'account_id':self.picking_type_id.account_id.id})



		if self.picking_type_id.code == 'incoming' and self.analytic_account_id.id:
			credit_line_vals.update({'analytic_account_id':self.analytic_account_id.id})
			
		if self.picking_type_id.code == 'incoming':
			if self.picking_type_id.account_id:
				credit_line_vals.update({'account_id':self.picking_type_id.account_id.id})

		res = [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
		if credit_value != debit_value:
			# for supplier returns of product in average costing method, in anglo saxon mode
			diff_amount = debit_value - credit_value
			price_diff_account = self.product_id.property_account_creditor_price_difference
			if not price_diff_account:
				price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
			if not price_diff_account:
				raise UserError(_('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))
			price_diff_line = {
				'name': self.name,
				'product_id': self.product_id.id,
				'quantity': qty,
				'product_uom_id': self.product_id.uom_id.id,
				'ref': self.picking_id.name,
				'partner_id': partner_id,
				'credit': diff_amount > 0 and diff_amount or 0,
				'debit': diff_amount < 0 and -diff_amount or 0,
				'account_id': price_diff_account.id,
			}
			if self.analytic_account_id.id:
				price_diff_line.update({'analytic_account_id':self.analytic_account_id.id})
			res.append((0, 0, price_diff_line))
		return res

class StockPicking(models.Model):
	_inherit = "stock.picking"

	account_available = fields.Boolean("check account id available or not",copy=False,compute='_compute_account_id',store=True)
	state = fields.Selection([
		('draft', 'Draft'),
		('holding','Go For Approval'),
		('approved','Approval'),
		('waiting', 'Waiting Another Operation'),
		('confirmed', 'Waiting'),
		('assigned', 'Ready'),
		('done', 'Done'),
		('cancel', 'Cancelled'),
	], string='Status', compute='_compute_state',
		copy=False, index=True, readonly=True, store=True, track_visibility='onchange',
		help=" * Draft: not confirmed yet and will not be scheduled until confirmed.\n"
			 " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows).\n"
			 " * Waiting: if it is not ready to be sent because the required products could not be reserved.\n"
			 " * Ready: products are reserved and ready to be sent. If the shipping policy is 'As soon as possible' this happens as soon as anything is reserved.\n"
			 " * Done: has been processed, can't be modified or cancelled anymore.\n"
			 " * Cancelled: has been cancelled, can't be confirmed anymore.")


	def waiting_to_ready(self):
		if self.state=="draft":
			self.state='holding'

	def waiting_to_approved(self):
		if self.state=="holding":
			self.state='approved'

	@api.depends('picking_type_id')
	def _compute_account_id(self):
		for picking in self:
			if picking.picking_type_id.account_id:
				picking.account_available = True
			else:
				picking.account_available = False



	# @api.multi
	# @api.depends('state', 'move_lines')
	# def _compute_show_mark_as_todo(self):
	# 	for picking in self:
	# 		if not picking.move_lines and not picking.package_level_ids:
	# 			picking.show_mark_as_todo = False
	# 		elif not (picking.immediate_transfer) and picking.state == 'approved':
	# 			picking.show_mark_as_todo = True
	# 		elif picking.state != 'approved' or not picking.id:
	# 			picking.show_mark_as_todo = False
	# 		else:
	# 			picking.show_mark_as_todo = True

	# @api.multi
	# def action_confirm(self):
	# 	self.mapped('package_level_ids').filtered(lambda pl: pl.state == 'approved' and not pl.move_ids)._generate_moves()
	# 	# call `_action_confirm` on every draft move
	# 	self.mapped('move_lines')\
	# 		.filtered(lambda move: move.state == 'approved')\
	# 		._action_confirm()
	# 	# call `_action_assign` on every confirmed move which location_id bypasses the reservation
	# 	self.filtered(lambda picking: picking.location_id.usage in ('supplier', 'inventory', 'production') and picking.state == 'confirmed')\
	# 		.mapped('move_lines')._action_assign()
	# 	return True
	

	def button_validate(self):
		sale_list=[]
		ref = self.name
		sale_analytic_dict={}
		purchase_analytic_dict={}
		if self.sale_id and self.company_id.anglo_saxon_accounting == False:
			for line in self.move_lines:
				if line.analytic_account_id:
					tag_ids = []
					for tag_id in line.tag_ids:
						tag_ids.append(tag_id.id)

					sale_analytic_dict.update({
						'name': line.sale_line_id.product_id.name,
						'amount': line.sale_line_id.price_unit,
										'product_id': line.sale_line_id.product_id.id,
						'product_uom_id': line.sale_line_id.product_uom.id,
						'date': line.date_expected,
						'account_id': line.analytic_account_id.id,
						'unit_amount': line.product_uom_qty,
						'general_account_id': self.partner_id.property_account_receivable_id.id,
						'ref': ref,
												'tag_ids':[(6,0,tag_ids)]
					})

					self.env['account.analytic.line'].create(sale_analytic_dict)


		if self.purchase_id and self.company_id.anglo_saxon_accounting == False:
			for line in self.move_lines:
				if line.analytic_account_id:
					tag_ids = []    
					for tag_id in line.tag_ids:
						tag_ids.append(tag_id.id)  

					purchase_analytic_dict.update({
						'name': line.purchase_line_id.product_id.name,
						'date': line.date_expected,
						'account_id': line.analytic_account_id.id,
						'unit_amount': line.product_uom_qty,
						'amount': (line.product_id.standard_price *line.product_uom_qty) * -1,
						'product_id': line.purchase_line_id.product_id.id,
						'product_uom_id': line.purchase_line_id.product_uom.id,
						'general_account_id': self.partner_id.property_account_payable_id.id,
						'ref': ref,
						'tag_ids':[(6,0,tag_ids)]
					})
					self.env['account.analytic.line'].create(purchase_analytic_dict)

		if not self.purchase_id and not self.sale_id:
			for line in self.move_lines:
				if line.analytic_account_id:
					tag_ids =[]
					for tag_id in line.tag_ids:
						tag_ids.append(tag_id.id)  
					if self.company_id.anglo_saxon_accounting == False:
						purchase_analytic_dict.update({
							'name': line.product_id.name,
							'date': datetime.now(),
							'account_id': line.analytic_account_id.id,
							'unit_amount': line.product_uom_qty ,
							'amount': line.product_id.lst_price * line.product_uom_qty ,
							'product_id': line.product_id.id,
							'product_uom_id': line.product_uom.id,
							'general_account_id': self.partner_id.property_account_receivable_id.id,
							'ref': ref,
							'tag_ids':[(6,0,tag_ids)] 
						})
						if self.picking_type_id.code == 'incoming':
							purchase_analytic_dict['amount']= (line.product_id.standard_price *line.product_uom_qty) * -1 
								 
						self.env['account.analytic.line'].create(purchase_analytic_dict)
		return super(StockPicking, self).button_validate()


class StockPickingTypeInherit(models.Model):
	_inherit = "stock.picking.type"

	project_id = fields.Many2one('project.project',string="Project")
	account_id = fields.Many2one('account.account',string="Account")



class PurchaseOrder(models.Model):
	_inherit = "purchase.order.line"

	def _prepare_stock_moves(self, picking):
		""" Prepare the stock moves data for one order line. This function returns a list of
		dictionary ready to be used in stock.move's create()
		"""
		self.ensure_one()
		res = []
		if self.product_id.type not in ['product', 'consu']:
			return res
		qty = 0.0
		price_unit = self._get_stock_move_price_unit()
		for move in self.move_ids.filtered(lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
			qty += move.product_qty
		template = {
			'name': self.name or '',
			'product_id': self.product_id.id,
			'product_uom': self.product_uom.id,
			'date': self.order_id.date_order,
			'date_expected': self.date_planned,
			'location_id': self.order_id.partner_id.property_stock_supplier.id,
			'location_dest_id': self.order_id._get_destination_location(),
			'picking_id': picking.id,
			'partner_id': self.order_id.dest_address_id.id,
			'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
			'state': 'draft',
			'purchase_line_id': self.id,
			'company_id': self.order_id.company_id.id,
			'price_unit': price_unit,
			'picking_type_id': self.order_id.picking_type_id.id,
			'analytic_account_id':self.account_analytic_id.id,
			'tag_ids':self.analytic_tag_ids and [(6, 0, [x.id for x in self.analytic_tag_ids])] or [],  

			'group_id': self.order_id.group_id.id,
			'origin': self.order_id.name,
			# 'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
			# 'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
		}


		diff_quantity = self.product_qty - qty
		if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
			template['product_uom_qty'] = diff_quantity
			res.append(template)
		return res
		
