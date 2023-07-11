from kafka import KafkaProducer
import json


if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers='jackarian-iot.it:9093',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                             key_serializer=str.encode,
                             security_protocol='SASL_PLAINTEXT',
                             sasl_mechanism='PLAIN',
                             sasl_plain_username='jackarian',
                             sasl_plain_password='MfFeZcJcZtdej6N')
    producer.send('temperatura-umidita-casa', key='cucina', value={
        'ambiente': 'cucina',
        'timestamp': '2023-01-01T12:12:00',
        'gradi': '78',
        'umidita': '80',
    })
    producer.flush()
