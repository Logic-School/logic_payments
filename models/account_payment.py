from odoo import fields, models, api

class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
        ('student', 'Student'),
        ('employee','Employee'),
    ], default='customer', tracking=True, required=True)
    payment_request_id = fields.Many2one('payment.request',string="Payment Request")
    