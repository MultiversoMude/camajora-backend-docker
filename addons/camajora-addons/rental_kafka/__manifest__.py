# Copyright 2020 jackarian iot srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Camajora Rental Kafka Topics',
    'description': """Kafka Topics""",
    'version': '12.0.2.0.0',
    'license': 'AGPL-3',
    'author': 'Giacomo Arianna',
    'website': 'https://jackarian-iot.it',
    'depends': ['rental'],
    'data': [
        'views/rental_kafka_configuration.xml',
        'security/rental_kafka_configuration.xml',
        'views/menu.xml'
    ],
    'demo': []
}
