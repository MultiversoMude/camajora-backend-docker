# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Camajora Website',
    'description': """Website CMS""",
    'version': '17.0.1.0',
    'license': 'AGPL-3',
    'author': 'Metadonors Srl',
    'website': 'https://www.metadonors.it',
    'application': True,
    'depends': [
        'api_base',
    ],
    'data': [
        'data/home_config_data.xml',
        'security/home_config.xml',
        'views/home_config.xml',
        'views/menu.xml',
    ],
    'assets': {},
    'demo': []
}
