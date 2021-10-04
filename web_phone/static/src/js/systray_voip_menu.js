odoo.define('web_phone.SystrayVoipMenu', function (require) {
    "use strict";
    const core = require('web.core');
    const session = require('web.session');
    const SystrayMenu = require('web.SystrayMenu');
    const Widget = require('web.Widget');

    const SystrayVoipMenu = Widget.extend({
        name: 'voip',
        template: 'web_phone.switch_panel_top_button',
        events: {
            'click': '_onClick',
        },

        /**
         * @override
         */
        async willStart() {
            const _super = this._super.bind(this, ...arguments);
            const isEmployee = await session.user_has_group('base.group_user');
            if (!isEmployee) {
                return Promise.reject();
            }
            return _super();
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onClick(ev) {
            ev.preventDefault();
            core.bus.trigger('voip_onToggleDisplay');
        },
    });

    // Insert the Voip widget button in the systray menu
    SystrayMenu.Items.push(SystrayVoipMenu);

    return SystrayVoipMenu;
});
