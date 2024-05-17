import datetime
from odoo import  api, fields, models
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment'
    _description = 'Cancel Appointment'

    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Janji temu')
    reason = fields.Text(string='Alasan')
    date_cancel = fields.Date(string='Tanggal pembatalan')

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
       
        return res

    
    def action_cancel(self):
        if self.appointment_id.booking_date == fields.date.today():
            raise ValidationError("Maaf, hari pembatalan tidak boleh sama dengan booking")
        self.appointment_id.state = 'batal'
        return
            
        
    
    
    
    