from odoo import models, fields, api

GENDER_SELECTION = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
]
CERTIFICATE_SELECTION = [
    ('elementary School', 'Elementary School'),
    ('junior high school', 'Junior High School'),
    ('graduate', 'Senior High School'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('doctor', 'Doctor'),
    ('other', 'Other'),
]


class HrFamilyInfo(models.Model):
    _name = 'hr.family.info'
    _inherit = 'phone.validation.mixin'
    _description = 'Employee Family Information'

    identification_id = fields.Char('Identification Id')
    name = fields.Char('Name', required='1')
    gender = fields.Selection(GENDER_SELECTION, 'gender')
    birthday = fields.Date('Date Of Birth')
    relation_id = fields.Many2one('hr.employee.relation', 'Relation')
    mobile = fields.Char('Mobile')
    certificate = fields.Selection(CERTIFICATE_SELECTION, 'Certificate Level',
                                   default='other', groups="hr.group_hr_user")
    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select corresponding Employee',
                                  invisible=1)
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', related='employee_id.country_id')

    @api.onchange('mobile', 'country_id')
    def _onchange_mobile_validation(self):
        if self.mobile:
            self.mobile = self.phone_format(self.mobile)


class HrEmployeeRelation(models.Model):
    _name = 'hr.employee.relation'
    _description = 'Relation'

    name = fields.Char('Name')
    abbreviation = fields.Char('Abbreviation')


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    spouse_identification_id = fields.Char('Identification Id')
    family_ids = fields.One2many(
        'hr.family.info', 'employee_id', string='Family', help='Family Information')
    certificate = fields.Selection(CERTIFICATE_SELECTION, 'Certificate Level',
                                   default='other', groups="hr.group_hr_user", tracking=True)
