{
    'name': "Payments",
    'author': 'Rizwaan',
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base','mail', 'account','logic_base','faculty','logic_sfc'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/payment_request_views.xml',
        'views/account_payment_views.xml',
        'wizard/register_pay_wizard_views.xml',
        'data/activity.xml',
    ],
    'demo': [],
    'summary': "Payments",
    'description': "Logic Payments",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}