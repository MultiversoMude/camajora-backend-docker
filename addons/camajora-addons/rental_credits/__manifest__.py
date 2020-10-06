# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Rental Credits',
    'description': """
        Camajora rental credit system""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Metadonors Srl',
    'website': 'https://www.metadonors.it',
    'depends': [
        'base',
        'account',
        'product',
        'rental',
    ],
    'data': [
        'views/res_partner.xml',
        'views/product_template.xml',
        'views/rental_resource.xml',
        # 'views/rental_booking_slot.xml',
        'views/rental_booking.xml',
        'data/product_template_data.xml',
    ],
    'demo': []
}
