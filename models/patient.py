from datetime import date
from odoo import  api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class HostpitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nama Pasien', tracking=True)
    date_of_birth = fields.Date(string='Tanggal Lahir')
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string='Janjitemu')
    age = fields.Integer(string='Umur', compute='_compute_age' , inverse='_inverse_compute_age',tracking=True, search='_search_age')
    ref = fields.Char(string='Refrensi')
    gender = fields.Selection(string='Gender', selection=[('laki-laki', 'Laki-laki'), ('perempuan', 'Perempuan'),], tracking=True)
    active = fields.Boolean(string='Active', default=True )
    image = fields.Image(string='image')
    tag_ids = fields.Many2many(comodel_name='patient.tag', string='Tags')
    appointment_count = fields.Integer(string='Jumlah pertemuan', compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Janjitemu')
    parent = fields.Char(string='Orang tua')
    marital_status = fields.Selection(string='Status Menikah', selection=[('menikah', 'Menikah'), ('belum_menikah', 'Belum Menikah'),], tracking=True)
    partner_name = fields.Char(string='Nama Pasangan')

    
    
    
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        appointment_group= self.env['hospital.appointment'].read_group(domain=[], fields=['patient_id'], groupby=['patient_id'])
        for appointment in appointment_group:
            patient_id = appointment.get('patient_id')[0]
            patient_rec = self.browse(patient_id)
            patient_rec.appointment_count = appointment ['patient_id_count']
            self -= patient_rec
        self.appointment_count=0
        

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super (HostpitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequnce'].next_by_code('hospital.patient')
        return super(HostpitalPatient, self).write(vals)
    
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Tanggal lahir yang dimasukkan tidak dapat diterima !"))
            
        
        
    
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        print("self..........", self)
        for rec in self:
            today= date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age= 1 

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta(years=rec.age)

    def _search_age(self, oporator, value):
        date_of_brith = date.today() - relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1,month=1)
        end_of_year = date_of_birth.replace(day=31,month=12)
        return[('date_of_birth', '>=', 'start_of_year'), ('date_of_birth', '<=', 'end_of_year')]
        
            
        

    def name_get(self):
        return [(record.id, "[%s] %s" %(record.ref, record.name)) for record in self]

        # patient_list = []
        # for record in self:
        #     name = record.ref + ' ' +record.name
        #     patient_list.append((record.id, name))

            
        

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("Kamu tidak bisa menghapus pasien dengan pertemuan"))
    
   
        
    
    def action_test(self):
        print ('clicked')
        return
    
    def action_done(self):
        return
        
        
        
    