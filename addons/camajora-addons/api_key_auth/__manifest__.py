# -*- coding: utf-8 -*-
# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Api Key Auth',
    'description': 'Authentication with Api Key in headers',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Metadonors srl',
    'website': 'https://www.metadonors.it',
    'depends': [
        'base_rest',
    ],
    'data': [
        'security/auth_api_token.xml',
        'views/auth_api_token.xml',
    ],
    'demo': [],
}
