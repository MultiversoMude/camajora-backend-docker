from odoo import fields, api, models, _
import logging

_logger = logging.getLogger(__name__)


class RentalLocation(models.Model):
    _inherit = 'rental.location'

    kafka_configuration = fields.Many2one("rental.kafka.configuration", string=_('Kafka Topics'))

    


