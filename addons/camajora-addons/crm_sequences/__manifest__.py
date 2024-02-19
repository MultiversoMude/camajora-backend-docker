# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Crm Sequences',
    'description': 'Add Sequence Code to CRM Entities',
    'version': '17.0.1.0',
    'license': 'AGPL-3',
    'author': 'Metadonors Srl',
    'website': 'https://www.metadonors.it',
    'depends': [
        'crm',
    ],
    'data': [
        'views/res_partner.xml',
        'views/crm_lead.xml',
        'data/crm_sequences.xml',
    ],
    'demo': [],
}
