odoo.define('show_form_view_after_search.AbstractController', function (require) {
    "use strict";

    var AbstractController = require('web.AbstractController');

     var includeDict = {
        reload: async function (params = {}) {
            var res = await this._super.apply(this, arguments);
            if (this.viewType === "kanban" || this.viewType === "list"){
                //if (this.renderer.state !== undefined && this.renderer.state.count === 1 && this.modelName === "product.template") {
                if (this.renderer.state !== undefined && this.renderer.state.count === 1) {
                    var $o_record = this.renderer.$el.find('.o_data_row,.o_kanban_record').not( ".o_kanban_ghost" );
                    if ($o_record.length === 1) {
                        $o_record.trigger("click");
                    }
                }
            }
            return res;
        },
    };
    AbstractController.include(includeDict);

});
