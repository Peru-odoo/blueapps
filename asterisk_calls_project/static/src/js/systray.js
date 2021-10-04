odoo.define('asterisk_calls_project.systray', function (require) {
"use strict";

var CallsMenu = require('asterisk_calls.systray');

var ProjectCallsMenu = CallsMenu.include({

    start: function () {
        this._updateButtonsHandlers();
        return this._super();
    },

    _updateButtonsHandlers: function() {
        this._super();
        var self = this;
        // Lead field
        this.$('tbody tr td[id="asterisk_calls_systray_project_td"]').off().on('click', function(ev){
            var project = $(ev.target).getAttributes().project;
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: "project.project",
                res_id: parseInt(project),
                views: [[false, 'form']],
                target: 'current',
                context: {},
            });
        });

        this.$('tbody tr td[id="asterisk_calls_systray_task_td"]').off().on('click', function(ev){
            var task = $(ev.target).getAttributes().task;
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: "project.task",
                res_id: parseInt(task),
                views: [[false, 'form']],
                target: 'current',
                context: {},
            });
        });
    },

});

return ProjectCallsMenu;

});
