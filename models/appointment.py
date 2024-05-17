
from odoo import  api, fields, models, _
from odoo.exceptions import ValidationError


class HostpitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string='Sequence', tracking=True)
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Pasien')
    gender = fields.Selection(string='Gender', selection=[('laki-laki', 'Laki-laki'), ('perempuan', 'Perempuan'),], related='patient_id.gender')
    ref = fields.Char(string='Refrensi', related='patient_id.ref')
    prescription = fields.Html(string='Resep')
    pharmacy = fields.Html(string='Farmasi')
    
    
    appointment_time = fields.Datetime(string='Waktu janji temu', default= fields.Datetime.now )
    booking_date = fields.Date(string='Waktu Booking', default= fields.Date.context_today)
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('konsultasi', 'Sedang Konsultasi'), ('done', 'Selesai'), ('batal', 'Batal'),] 
    , default='draft', required=True)
    doctor_id = fields.Many2one(comodel_name='res.users', string='Dokter')
    pharmacy_line_ids = fields.One2many(comodel_name='appointment.pharmacy.lines', inverse_name='appointment_id', string='Farmasi')
    hide_sales_price = fields.Boolean(string='Sembunyikan harga')
    duration = fields.Float(string='durasi')
    
    
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super (HostpitalAppointment, self).create(vals)
    
    def action_test(self):
        print("Button !!!!!!!!!!")
        return{
            'effect':{
                'fadeout': 'slow',
                'message': 'Cilck Successful',
                'type': 'rainbow_man'
            }
        }
    
    def action_konsultasi(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'konsultasi'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_batal(self):
        action = self.env.ref('om_hospital.cancel_appointment_action').read()[0]
        return action
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def unlink(self):
        if self.state == 'done':
            raise ValidationError (_('Catatan telah disetel ke Selesai dan tidak dapat dihapus. '))
        return super(HostpitalAppointment, self).unlink()

              
       
        
        
class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one(comodel_name='product.product', string='Produk', required=True)
    price_unit = fields.Float(string='Harga', related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default= 1)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Janji temu')
    
    
    
  
        