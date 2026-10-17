# Copyright 2021 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResourceImageRelation(models.Model):
    _name = "resource.image.relation"
    _inherit = "image.relation.abstract"
    _description = "Resource Image Relation"

    resource_id = fields.Many2one("rental.resource")
    tag_id = fields.Many2one("image.tag", domain=[("apply_on", "=", "resource")])
