from odoo import api, fields, models, _
from ..producer.location_producer import InstanceMessageProducer
import logging

_logger = logging.getLogger(__name__)


class RentalResourceInstance(models.Model):
    _inherit = 'rental.resource.instance'

    @api.model
    def create(self, vals):
        _logger.debug("Test kafka send:%s", vals)
        resource_instance = super().create(vals)

        resource = self.env['rental.resource'].search([('id', '=', resource_instance.resource_id.id)])
        location = resource.location_id
        configuration = location.kafka_configuration

        _logger.debug("Test kafka send: location %s", location)
        _logger.debug("Test kafka send: location %s", configuration)
        _logger.debug("Test kafka send: location %s", configuration)

        producer = InstanceMessageProducer(configuration, resource_instance, location, resource)
        producer.sendToKafka()
        return resource_instance
