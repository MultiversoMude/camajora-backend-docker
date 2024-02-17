from kafka import KafkaProducer
import json
import logging

_logger = logging.getLogger(__name__)


class InstanceMessageProducer:
    def __init__(self, channel_configuration, instance, location, resource):
        self.channel_configuration = channel_configuration
        self.instance = instance
        self.location = location
        self.resource = resource

    def sendToKafka(self):
        try:
            if self.channel_configuration is not None:
                _logger.debug("Instance queued")
                producer = self._buildProducer()
                producer.send(self.channel_configuration['topic'], key=str(self.location['id']),
                              value=self._serializeData())
                producer.flush()
        except Exception:
            _logger.debug("Failed sending info to Kafka")
            _logger.debug("Current configuration %s", self.channel_configuration)
            _logger.debug("-> location %s", self.location)
            _logger.debug("-> instance %s", self.instance)
            _logger.debug("-> resource %s", self.resource)

    def _serializeData(self):
        return {
            'location_id': self.location['id'],
            'location_name': self.location['name'],
            'scc_address': self.location['scc_address'],
            'resource_name': self.resource['name'],
            'resource_code': self.resource['code'],
            'resource_modbus_group': self.resource['modbus_group'],
            'resource_modbus_modbus_id': self.resource['modbus_id'],
            'resource_modbus_modbus_plugin': self.resource['modbus_plugin'],
            'resource_instance_code': self.instance['code'],
        }

    def _buildProducer(self):
        return KafkaProducer(bootstrap_servers=self.channel_configuration['bootstrap_servers'],
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                             key_serializer=str.encode,
                             security_protocol=self.channel_configuration['security_protocol'],
                             sasl_mechanism=self.channel_configuration['sasl_mechanism'],
                             sasl_plain_username=self.channel_configuration['sasl_plain_username'],
                             sasl_plain_password=self.channel_configuration['sasl_plain_password'], )


if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers='jackarian-iot.it:9093',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                             key_serializer=str.encode,
                             security_protocol='SASL_PLAINTEXT',
                             sasl_mechanism='PLAIN',
                             sasl_plain_username='jackarian',
                             sasl_plain_password='MfFeZcJcZtdej6N')
    producer.send('location-consumption', key=str(1), value={
        'ambiente': 'soggiorno',
        'timestamp': '2023-01-01T12:12:00',
        'gradi': 78,
        'umidita': '80',
    })
    producer.flush()
