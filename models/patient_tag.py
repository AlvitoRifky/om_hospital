from odoo import  api, fields, models, _
from odoo.exceptions import ValidationError


class HostpitalPatient(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Nama', required=True)
    active = fields.Boolean(string='Active', default=True, copy=False)
    color = fields.Integer(string='Warna')
    color_2 = fields.Char(string='Warna 2')
    sequence = fields.Integer(string='Sequence')


    _sql_constraints = [
        ('name_uniq', 'unique (name, active)','testing !'),
        ('check_sequence', 'check (sequence > 0)','sequence harus diatas 0')
    ]
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        default['sequence'] = 10
        return super(HostpitalPatient, self).copy(default)
    
    