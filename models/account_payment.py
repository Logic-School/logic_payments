from odoo import fields, models, api,_

class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
        ('student', 'Student'),
        ('employee','Employee'),
    ], default='customer', tracking=True, required=True)
    payment_request_id = fields.Many2one('payment.request',string="Payment Request")

    def _prepare_payment_display_name(self):
        result = super(AccountPaymentInherit,self)._prepare_payment_display_name()
        result['outbound-student'] = _('Student Payment')
        return result