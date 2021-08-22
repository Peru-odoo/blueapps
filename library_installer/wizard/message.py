# -*- coding: utf-8 -*-
##################################################
#                                                #
#    Cyb3rSky Corp. (A group for freelancers)    #
#    Copyright (C) 2021 onwards                  #
#                                                #
#    Email: cybersky25@gmail.com                 #
#                                                #
##################################################

from odoo import models, fields


class MessageWizard(models.TransientModel):
    _name = 'message.wizard'
    _description = "Success Message Wizard"

    message = fields.Text('Message', required=True)

    def status_ok(self):
        return {'type': 'ir.actions.act_window_close'}