from odoo import  api, fields, models


class HostpitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female'),])
    
    
    
    