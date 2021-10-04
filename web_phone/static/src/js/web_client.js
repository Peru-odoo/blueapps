odoo.define('web_phone.WebClient', function (require) {
    "use strict";

    const DialingPanel = require('web_phone.DialingPanel');
    const WebClient = require('web.WebClient');

    WebClient.include({
        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------
        /**
         * @override
         */
        async show_application() {
            await this._super(...arguments);
            this._dialingPanel = new DialingPanel(this);
            await this._dialingPanel.appendTo(this.$el);
        },
    });
});
