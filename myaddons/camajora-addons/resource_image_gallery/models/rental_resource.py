# Copyright 2021 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RentalResource(models.Model):
    _inherit = "rental.resource"

    image_small_url = fields.Char(
        related="image_ids.image_id.image_small_url", store=True
    )
    image_medium_url = fields.Char(
        related="image_ids.image_id.image_medium_url", store=True
    )
    image_ids = fields.One2many(
        "resource.image.relation", inverse_name="resource_id", string="Images"
    )
