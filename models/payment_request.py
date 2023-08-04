from odoo  import fields, api, models

class PaymentRequest(models.Model):
    _name = "payment.request"
    # _rec_name="number"
    def _compute_number(self):
        for record in self:
            zeroes = "0"*(5 - len(str(record.id)))
            record.name = "PAY-RQ-"+str(record.create_date.year)+"/"+str(record.create_date.month)+"/"+zeroes+str(record.id)
    name=fields.Char(string="Number",compute="_compute_number")
    source_type = fields.Selection(selection=[('other','Other'),('advance','Advance'),('sfc','Student Faculty Club')],string="Source Type")
    sfc_source = fields.Many2one('student.faculty',string="SFC Source",readonly=True)
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

    state = fields.Selection(string="State",selection=[('payment_request','Payment Requested'),('payment_draft','Payment Drafted'),('paid','Paid'),('reject','Rejected'),('cancel','Cancelled')])
    description = fields.Text(string="Description")
    account_name = fields.Char(string="Account Name")
    account_no = fields.Char(string="Account No")
    ifsc_code = fields.Char(string="IFSC Code")
    bank_name = fields.Char(string="Bank Name")
    bank_branch = fields.Char(string="Bank Branch")
    payments = fields.One2many('account.payment','payment_request_id',string="Payments")
    
    def _compute_payment_count(self):
        for record in self:
            record.payment_count = len(record.payments)
    payment_count = fields.Integer(string="Payments Count",compute="_compute_payment_count")
    
    @api.model
    def create(self, vals):
        vals['state'] = 'payment_request'
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
            'context': {'amount': self.amount,'payment_request_id':self.id ,'partner_type':partner_type}
        }
    def reject_payment(self):
        self.state = 'reject'
        self.sfc_source.write({
            'state':'reject'
        })