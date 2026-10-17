from odoo import fields, models, _


class RentalKafkaConfiguration(models.Model):
    _name = 'rental.kafka.configuration'
    _description = 'Rental Kafka Topic Configuration'

    name = fields.Char(string=_('Name'))
    model = fields.Char(string=_('Related Model'))
    description = fields.Char(string=_('Description'))
    security_protocol = fields.Char(string=_('Security Protocol'))
    sasl_mechanism = fields.Char(string=_('Sasl Mechanism'))
    sasl_plain_username = fields.Char(string=_('Sasl plain username'))
    sasl_plain_password = fields.Char(string=_('Sasl plain password'))
    bootstrap_servers = fields.Char(string=_('Bootstrap servers'))
    topic = fields.Char(string=_('Topic '))
