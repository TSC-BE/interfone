# Copyright 2019 Salinity Developers <http://salinity.in/>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': "Interfone Connect",
    'version': '16.0.0.1.0',
    'sequence': 16,
    'category': 'Extra Tools',
    'author': "The Service Company",
    'website': 'https://www.tsc-experts.com/',
    'depends': ['contacts', 'web_notify', 'phone_validation'],
    'data': [
        'views/res_users_views.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [],
    'test': [],
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
}
