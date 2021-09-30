from odoo import fields, models, api

import urllib3
import json


class NotesNote(models.Model):
    _name = 'notes.note'
    _description = 'Description'

    partner_id = fields.Many2one('res.partner', name="Note By")
    note = fields.Text(name="Note")
    time_date = fields.Datetime(string="Time")

    def get_notes(self):
        http = urllib3.PoolManager()
        URL = 'http://www.example.com'
        root = '/notes/note'  # the path where the request handler is located
        datas = http.request('GET', URL + root)
        datas = json.loads(datas.data.decode('utf-8'))  # parses the response to  a compatible form
        for data in datas:
            self.env['notes.note'].create({
                'partner_id': self.env['res.partner.search'].search([('notes_user_id', '=', data['user_id'])]).id,
                'note': data['note'],
                'time_date': data['time']
            })
