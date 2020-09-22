odoo.define('odoo_e_wallet.odoo_e_wallet_js', function (require) {
'use strict';
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
    var ajax = require('web.ajax');
    var PaymentForm = require('payment.payment_form');

    PaymentForm.include({
        payEvent: function(ev) {
            ev.preventDefault();
            var self = this;

            // TODO: self._super().apply(self, args) not working, so need to implement this
            var pf_super = self._super;
            var args = arguments;
            // ----------------------------------------------------------------------------

            var pay_using_wallet = $('#wallet_payment #pay_using_wallet').prop('checked');
            if ( pay_using_wallet ) {
                ajax.jsonRpc('/wallet/check/status', 'call', { 
                    'is_checked': pay_using_wallet,
                })
                .then(function(res) {
                    if ( res.is_safe ) {
                        return pf_super.apply(self, args);
                    } else {
                        location.reload();
                    }
                });
            } else {
                return self._super.apply(self, arguments);
            }
        }
    }) 

    $(document).ready(function() {
        const $pay_using_wallet = $('#pay_using_wallet');
        var isSubmit = 0; // 0 == page refresh, 1 == #pay_using_wallet clicked
        var cur_lang = $('html').attr('lang');
        var loc_url = $(location).attr("href");
        const $wallet_acq = $('#payment_method input[data-provider="e_wallet"]');
        /// Initially We disable the wallet acq & enable it when pay using wallet is triggered
        $wallet_acq.prop('checked', false);
        // const $wallet_acq = $('#payment_method input[data-provider="e_wallet"]');
        function placeholder() {
            let placeholder = '';
            if(localStorage.getItem('selection') == 'sale_order'){
                $('#wk_input').attr("placeholder","Sale Order ID...");
            }
            else if(localStorage.getItem('selection') == 'transaction_id'){
                $('#wk_input').attr("placeholder","Transaction ID...");
            }
            else if(localStorage.getItem('selection') == 'all'){
                $('#wk_input').val('');
                $('#wk_input').attr("placeholder","Search...");
            }
        }

        if(localStorage.getItem('selection') == null){
            localStorage.setItem('selection','sale_order');
            $('#wk_input').attr("placeholder","Search...");
        }
        else{
            placeholder();
        }

        $('#wallet_selection').click(function(){
            localStorage.setItem('selection',$('option:selected', this).attr('value'));
            placeholder();
        });

        // Checkbox Condition
        // Rest wallet debit in case of page reload on payment page
        // Need to fire before page load, as rpc takes time & view doesn't updated well with the new updated values
        $(window).on("beforeunload", function() {
            var loc_url = $(location).attr("href");
            if(loc_url.includes('/shop/payment') && isSubmit != 1) {
		        $.blockUI({ css: { backgroundColor: '#f00', color: '#fff'} });
                let $orderTotal = $('#order_total');
                $orderTotal.addClass('d-none');
                ajax.jsonRpc("/payment/add/wallet", 'call',{
                    'add_wallet': false
                }).then(function(data) {
                    $.unblockUI();
                })
            }
        });

        $(window).on('load', function () {
            if($pay_using_wallet.prop('checked')) {
                $pay_using_wallet.prop('checked', false);
            }
            if(localStorage.getItem('selection') != null && localStorage.getItem('selection')){
                $('#wallet_selection option[value='+localStorage.getItem("selection")+']').attr("selected", "selected");
            }
            // Special case: When user cancel an ongoing transaction
            if(loc_url.includes('/shop/payment')) {
                ajax.jsonRpc("/payment/add/wallet", 'call',{
                    'add_wallet': false
                });
            }

        })

        $pay_using_wallet.on('change',function() {
            let cur_checkbox = $(this);
            let add_wallet = cur_checkbox.is(':checked');

            $.blockUI({ css: { backgroundColor: '#f00', color: '#fff'} });
            
            $('#wallet_payment .card-body').find('.js_add_msg').remove();
            $('#payment_method > h3, #payment_method .card').removeClass('d-none');

            ajax.jsonRpc("/payment/add/wallet", 'call', {
                'add_wallet': add_wallet,
            })
            .then(function(data) {
                
                // Manage Acquirer JS
                // let walletIndependent = data.wallet_debit == data.amount_total ? true : false;
                // if ( walletIndependent && add_wallet ) {
                //     $wallet_acq.closest('.card').find('input[name="pm_id"]').prop('disabled', true);
                //     $wallet_acq.prop('disabled', false);
                //     $wallet_acq.prop('checked', true);
                // } else {
                //     $wallet_acq.closest('.card').find('input[name="pm_id"]').prop('disabled', false);
                //     $wallet_acq.prop('disabled', true);
                //     $wallet_acq.prop('checked', false);
                // }

                $('#wallet_payment #wallet_bal').remove();

                let walletIndependent = data.wallet_debit == data.amount_total ? true : false;

                if ( walletIndependent && add_wallet ) {
                    $('#payment_method > h3, #payment_method .card').addClass('d-none');
                    $wallet_acq.prop('checked', true);
                } else if ( !walletIndependent && add_wallet ) {
                    let message = 'Please select a payment acquirer to the pay remaining amount...';
                    let html = '<div class="bg-warning js_add_msg">'+ message +'</div>';
                    $('#wallet_payment .card-body').append(html);
                    $wallet_acq.prop('checked', false);
                } else {
                    $wallet_acq.prop('checked', false);
                }

                let $orderTotal = $('#order_total');
                let symbol = data.symbol;
                let position = data.position;
                if (data.wallet_debit == 0) {
                    $('#wallet_tr').remove();
                    $('#order_total_w').remove();
                    $('#wallet_payment .js_wallet_bal').html(data.used_wallet_amount_template);
                    $orderTotal.removeClass('d-none');
                } else {
                    $('#wallet_payment .js_wallet_bal').html(data.used_wallet_amount_template);

                    $orderTotal.before(data.wallet_total_template);

                    $orderTotal.addClass('d-none');
                    $('#wallet_tr').after(data.total_amount_template);
                }
                $.unblockUI();
            })
        });

        var $carriers = $("#delivery_carrier .o_delivery_carrier_select");
        $carriers.click(function() {
            if($pay_using_wallet.prop('checked')) {
                $.blockUI({ css: { backgroundColor: '#f00', color: '#fff'} });
                $pay_using_wallet.prop("checked", false);
                $pay_using_wallet.trigger('change');
            }
        });

        $('#o_payment_form_pay').on('click', function() {
            isSubmit = 1;
        });

    });
});
