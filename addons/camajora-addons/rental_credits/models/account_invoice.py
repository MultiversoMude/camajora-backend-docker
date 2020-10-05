# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_paid(self):
        res = super().action_invoice_paid()
        for invoice in self:
            invoice._generate_credit_order()

        return res

    @api.multi
    def _generate_credit_order(self):
        """
            This method is called upon payment of an order.
            It checks every single line of the sale order and if it finds a credit package
            assign the number of credits to the buyer.
        """
        sale_order_id = self.env['sale.order'].search([('name', '=', self.origin)])
        credits_to_add = 0

        for line in sale_order_id.order_line:
            if line.product_id.product_tmpl_id.is_credits:
                credits_to_add = credits_to_add + (
                    line.product_id.product_tmpl_id.credits_value * int(line.product_uom_qty)
                )

        sale_order_id.partner_id.write({
            'credits': sale_order_id.partner_id.credits + credits_to_add
        })
