from odoo import api, fields, models


class Note(models.Model):
	_inherit = 'note.note'

	@api.multi
	def act_back(self):
		if self._context.get('save_close'):
			return {'type': 'ir.actions.act_window_close'}
		return {'name': 'Notes',
				'type': 'ir.actions.act_window',
				'view_id': self.env.ref('note_quick.view_quick_note_kanban').id,
				'view_mode': 'kanban',
				'res_model': 'note.note',
				'target': 'new'}

	@api.model
	def act_create_one(self):
		return {'name': 'Create a new note',
				'type': 'ir.actions.act_window',
				'view_id': self.env.ref('note_quick.view_quick_note_form').id,
				'view_mode': 'form',
				'res_model': 'note.note',
				'target': 'new'}

	@api.multi
	def act_edit(self):
		return {'name': 'Edit Note',
				'type': 'ir.actions.act_window',
				'view_id': self.env.ref('note_quick.view_quick_note_form').id,
				'view_mode': 'form',
				'res_model': 'note.note',
				'res_id': self.id,
				'target': 'new'}
