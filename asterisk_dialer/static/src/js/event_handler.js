odoo.define("asterisk_dialer.call", function (require) {
    "use strict";
  
    var WebClient = require('web.WebClient');
    var ajax = require('web.ajax');
    var utils = require('mail.utils');
    var session = require('web.session');    
    var channel = 'dialer_operator_';

    WebClient.include({
        start: function(){
            this._super()
            self = this
            ajax.rpc('/web/dataset/call_kw/res.users', {
                    "model": "res.users",
                    "method": "read",
                    "args": [session.uid],
                    "kwargs": {'fields': ['dialer_operator_accountcode']},
            }).then(function (res) {
              self.accountcode = res[0].dialer_operator_accountcode
              if (self.accountcode) {
                // Start polling
                self.operator_channel = channel + self.accountcode
                self.call('bus_service', 'addChannel', self.operator_channel)
                self.call('bus_service', 'onNotification', self, self.asterisk_dialer_event_handler)
                console.log('asterisk_dialer: listening on ', self.operator_channel)
              }
            })
        },

        asterisk_dialer_event_handler: function (notification) {
          // console.log('asterisk_dialer_event_handler: ', notification)
          for (var i = 0; i < notification.length; i++) {
             var ch = notification[i][0]
             var msg = notification[i][1]
             if (ch == this.operator_channel) {
                 try {
                  this.asterisk_dialer_handle_message(msg)
                }
                catch(err) {console.log(err)}
             }
           }
        },

        asterisk_dialer_handle_message: function(msg) {
          // console.log('asterisk_dialer_handle_message: ', msg)
          if (typeof msg == 'string')
            var message = JSON.parse(msg)
          else
            var message = msg
          var action = this.action_manager && this.action_manager.getCurrentAction()
          if (!action) {
              console.log('Action not loaded')
              return
          }
          var controller = this.action_manager.getCurrentController()
          if (!controller) {
              console.log('Controller not loaded')
              return
          }          
          // Check if it's a call from partner to "me".
          // console.log(message);
          // console.log('Opening contact form')
          this.do_action({
            'type': 'ir.actions.act_window',
            'res_model': 'asterisk_dialer.contact',
            'target': 'main',
            'res_id': message.contact,
            'views': [[false, 'form']],
            // 'context': {'form_view_initial_mode': 'edit'}
            })
          return
        },
    })
})
