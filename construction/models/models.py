# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Construction(models.Model):
    _name = 'construction.construction'
    _description = 'construction'

    name = fields.Char()

