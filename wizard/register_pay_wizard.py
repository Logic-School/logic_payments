from odoo import fields,models,api
from datetime import datetime
class  PayWizard(models.TransientModel):
    _name="payment.register.wizard"
    journal = fields.Many2one('account.journal',string="Journal")
    recipient_bank = fields.Many2one('res.partner.bank',string="Recipient Bank Account")
    company_id = fields.Many2one(
            'res.company', store=True, copy=False,
            string="Company",
            default=lambda self: self.env.user.company_id.id,
            readonly=True)
    currency_id = fields.Many2one(
            'res.currency', string="Currency",
            related='company_id.currency_id',
            default=lambda
            self: self.env.user.company_id.currency_id.id,
            readonly=True)
    amount = fields.Monetary(string="Amount",default=lambda self: self._context.get('amount'))
    date = fields.Date(string="Date",default=datetime.today())
    pay_request_id = fields.Many2one('payment.request',string="Payment Request",default = lambda self: self._context.get('pay_request_id'))

    def action_create_payments(self):
        # need to add methods to create payment record in db
        pay_req_obj = self.env['payment.request'].search([('id','=',self.pay_request_id.id)])
        if pay_req_obj:
            pay_req_obj.write({
                'state':'paid',
            })
