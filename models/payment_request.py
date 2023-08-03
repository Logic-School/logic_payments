from odoo  import fields, api, models

class PaymentRequest(models.Model):
    _name = "payment.request"
    source_type = fields.Selection(selection=[('other','Other'),('advance','Advance'),('sfc','Student Faculty Club')],string="Source Type")
    sfc_source = fields.Many2one('student.faculty',string="SFC Source")
    source_user = fields.Many2one('res.users',string="Source User", default=lambda self: self.env.user)
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

    state = fields.Selection(string="State",selection=[('submit_payment','Submitted For Payment'),('paid','Paid'),('reject','Reject')])
    description = fields.Text(string="Description")
    account_name = fields.Char(string="Account Name")
    account_no = fields.Char(string="Account No")
    ifsc_code = fields.Char(string="IFSC Code")
    bank_name = fields.Char(string="Bank Name")
    bank_branch = fields.Char(string="Bank Branch")

    @api.model
    def create(self, vals):
        vals['state'] = 'submit_payment'
        result = super(PaymentRequest, self).create(vals)
        return result

    def register_payment(self):
        # Display a popup with the entered details
        if self.sfc_source:
            partner_type = 'student'
        else:
            partner_type = False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Register Payment',
            'res_model': 'payment.register.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'amount': self.amount,'payment_request_id':self.id,'partner_type':partner_type}
        }
    def reject_payment(self):
        self.state = 'reject'
        self.sfc_source.write({
            'state':'reject'
        })