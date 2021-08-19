odoo.define('web.note_tray', function(require){
"use strict";

var config = require('web.config');
var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var AbstractWebClient = require('web.AbstractWebClient');

var NoteTray = Widget.extend({
    template: 'NoteTray',
    events: {
        'click': '_onClick',
    },
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.isMobile = config.device.isMobile;
        this._onClick = _.debounce(this._onClick, 1500, true);
    },
    /**
     * @override
     */
    willStart: function () {
        return this._super();
    },
    /**
     * @override
     */
    start: function () {
      return this._super();
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClick: function (ev) {
        ev.preventDefault();
        var self = this;
        this.trigger_up('clear_uncommitted_changes', {
            callback: function () {
                self._rpc({
                        route: "/web/action/load",
                        params: {
                            action_id: "note_quick.action_quick_note"
                        },
                    })
                    .done(function (result) {
                      self.do_action(result);
                    });
            },
        });
    },
});

SystrayMenu.Items.push(NoteTray);
return NoteTray;
});