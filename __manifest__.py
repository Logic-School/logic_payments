{
    'name': "Payments",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'account','logic_base','logic_sfc'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_request_views.xml',
        'wizard/register_pay_wizard_views.xml',
    ],
    'demo': [],
    'summary': "Payments",
    'description': "",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}