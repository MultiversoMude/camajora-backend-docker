# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Rest Shop',
    'description': """
        REST Shop Services""",
    'version': '12.0.3.0.0',
    'license': 'AGPL-3',
    'author': 'Metadonors Srl',
    'website': 'https://www.metadonors.it',
    'depends': [
        'onchange_helper',
        'payment_stripe',
        'sale'
    ],
    'data': [
        # 'views/payment_acquirer.xml',
        'views/sale_order.xml',
        'data/sequences.xml',
    ],
    'demo': [
    ],
}
