# -*- coding: utf-8 -*-
##################################################
#                                                #
#    Cyb3rSky Corp. (A group for freelancers)    #
#    Copyright (C) 2021 onwards                  #
#                                                #
#    Email: cybersky25@gmail.com                 #
#                                                #
##################################################

from odoo import models, fields, _
import sys
import subprocess
import base64
from odoo.exceptions import UserError


class Installer(models.TransientModel):
    _name = "library_installer.installer"
    _description = "Python3 Library installer using"

    select_type = fields.Selection(
        [("text", "Textbox"), ("file", "Text File")], default="file")
    lib_data = fields.Text(
        help="Type the python libraries name separated by comma (,)", string="Library Name(s)")

    requirements_file = fields.Binary("Requirements file")

    def install(self):
        self.ensure_data()
        if self.requirements_file:
            file_data = base64.decodestring(self.requirements_file).decode("utf8")
            lib_data = " ".join(file_data.split("\n"))
        else:
            lib_data = " ".join(self.lib_data.split(','))
        
        cmd = sys.executable + " -m pip install --upgrade --user " + lib_data

        ps = subprocess.Popen(cmd, shell=True)
        exitcode = ps.wait()

        if exitcode != 0:
            raise UserError(
                "Went into an error while installing one or more libraries. The following could be the reasons:\n1) Misspelled library name.\n2) Library version not availabe.\n3) Library not available.")
        self.show_success()

    def ensure_data(self):
        if self.lib_data:
            return True
        elif self.requirements_file:
            return True
        raise UserError("Invalid input!")

    def show_success(self):
        message_id = self.env['message.wizard'].create({'message': _("Libraries were installed successfully.")})
        return {
            'name': _('Successfull'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'res_id': message_id.id,
            'target': 'new'
        }