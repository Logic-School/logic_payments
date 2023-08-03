from odoo  import fields, api, models

class PaymentRequest(models.Model):
    _name = "payment.request"
    source_type = fields.Selection(selection=[('advance','Advance'),('sfc','Student Faculty')],string="Source Type")
    sfc_source = fields.Many2one('student.faculty',string="SFC Source")
    source_user = fields.Many2one('res.users',string="Source User")
    amount = fields.Monetary(string="Amount")
    payment_expect_date = fields.Date(string="Expected Date")
    payment_date = fields.Date(string="Date of Payment", readonly=True)
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
    def _compute_state(self):
        for record in self:
            if not record.state:
                record.state = 'submit_payment'
            else:
                record.state = record.state
    state = fields.Selection(string="State",selection=[('submit_payment','Submitted For Payment'),('paid','Paid'),('reject','Reject')], compute = "_compute_state")
    description = fields.Text(string="Description")
    account_name = fields.Char(string="Account Name")
    account_no = fields.Char(string="Account No")
    ifsc_code = fields.Char(string="IFSC Code")
    bank_name = fields.Char(string="Bank Name")
    bank_branch = fields.Char(string="Bank Branch")

    def register_payment(self):
        # Display a popup with the entered details
        return {
            'type': 'ir.actions.act_window',
            'name': 'Register Payment',
            'res_model': 'payment.register.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'amount': self.amount,'pay_request_id':self.id}
        }
    def reject_payment(self):
        pass