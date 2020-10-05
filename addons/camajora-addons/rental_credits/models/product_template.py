# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    is_credits = fields.Boolean(string=_("Is credits product"), default=False)
    credits_value = fields.Integer(string=_("Credits value"))
