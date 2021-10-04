odoo.define('asterisk_calls_helpdesk.systray', function (require) {
"use strict";

var CallsMenu = require('asterisk_calls.systray');

var HelpdeskCallsMenu = CallsMenu.include({

    start: function () {
        this._updateButtonsHandlers();
        return this._super();
    },

    _updateButtonsHandlers: function() {
        this._super();
        var self = this;
        // Helpdesk field
        this.$('tbody tr td[id="asterisk_calls_systray_ticket_td"]').off().on('click', function(ev){
            var ticket = $(ev.target).getAttributes().ticket;
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: "helpdesk.ticket",
                res_id: parseInt(ticket),
                views: [[false, 'form']],
                target: 'current',
                context: {},
            });
        });
    },

});

return HelpdeskCallsMenu;

});
