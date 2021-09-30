
odoo.define('odoo_website_product_quote.web', function(require) {
    "use strict";
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;
    var sAnimations = require('website.content.snippets.animation');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var session = require('web.session');
    var Widget = require('web.Widget');
    var VariantMixin = require('sale.VariantMixin');
    var publicWidget = require('web.public.widget');   

    sAnimations.registry.websiteQuote = publicWidget.Widget.extend(VariantMixin, {
    
         selector: '.oe_website_sale',
        events: {    
            'change #txt': '_onChangeQty',
            'click .o_add_quote, .o_add_quote_dyn': '_onClickQuote',
            // 'click .o_add_quote_one': '_onClickQuote',          
            'click #bt_non':'_onNonlogin',
            // 'click .o_add_quote': '_onClickQuote',
            // 'change #country_id': '_onChangeCountry',
        },
        _onChangeQty: function () {
                var jsonObj = [];
                $('#tbl tbody tr').each(function(){
                    var in_val = $(this).find("#txt > input[type=text]").val();
                    var x = $(this).find('#txt').attr('line_id');
                    var item = {}
                    item [x] = in_val;
                    jsonObj.push(item); 
                    
                });
                var user = session.uid
                this._rpc({
                    route: "/shop/quote/update_json",
                    params: {
                        jsdata: jsonObj,
                    },
                });
        },
        
        _onClickQuote: function (ev) {
            this._addNewqProducts($(ev.currentTarget));
        },
        _addNewqProducts: function ($el) {
            var self = this;
            var productID = $el.data('product-product-id');            
            if ($el.hasClass('o_add_quote_dyn')) {
                productID = $el.parent().find('.product_id').val();
                if (!productID) { // case List View Variants
                    productID = $el.parent().find('input:checked').first().val();
                }
                productID = parseInt(productID, 10);                
            }
            var $form = $el.closest('form');
            var templateId = $form.find('.product_template_id').val();
            // when adding from /shop instead of the product page, need another selector
            if (!templateId) {
                templateId = $el.data('product-template-id');
            }
            $el.prop("disabled", true).addClass('disabled');
            var productReady = this.selectOrCreateProduct(
                $el.closest('form'),
                productID,
                templateId,
                false
            );

            productReady.then(function (productId) {
                productId = parseInt(productId, 10);
            
                if (productId) {                    
                    return self._rpc({
                        route: '/shop/quote/add',
                        params: {
                            product_id: productId,
                        },
                    }).then(function () {
                        // var $navButton = $('header .o_wsale_my_wish').first();
                        // self.wishlistProductIDs.push(productId);
                        // self._updateWishlistView();
                        // wSaleUtils.animateClone($navButton, $el.closest('form'), 25, 40);
                        window.location.href = '/shop/quote';
                    }).guardedCatch(function () {
                        $el.prop("disabled", false).removeClass('disabled');
                    });
                }
            }).guardedCatch(function () {
                $el.prop("disabled", false).removeClass('disabled');
            });
        },
        _onNonlogin: function () {
            var id1 = document.getElementById("txt1").value
            var obj = document.getElementById("obj").value
            ajax.jsonRpc("/shop/product/quote/confirm/nonlogin","call",{
                'id1' : id1,
                'obj':obj,
            }).then(function (data) {
                window.location.href = '/thank_you';
            });
        }
    });

    $(document).ready(function (){

        $("select[name='country_id]'").change(function() {
            var $country = this.$('select[name="country_id"]');
            var countryID = ($country.val() || 0);
            this.$stateOptions.detach();
            var $displayedState = this.$stateOptions.filter('[data-country_id=' + countryID + ']');
            var nb = $displayedState.appendTo(this.$state).show().length;
            this.$state.parent().toggle(nb >= 1);
        });
    });
});

odoo.define("website_rfq.recently_viewed", function (require) {
    "use strict";
    var core = require("web.core");
    var QWeb = core.qweb;
    var options = require("website_sale.recently_viewed");
    var ajax = require("web.ajax");
    var _t = core._t;
    var Dialog = require("web.Dialog");
    var publicWidget = require("web.public.widget");

    publicWidget.registry.productsRecentlyViewedSnippet.include({
        xmlDependencies: ["/website_rfq/static/src/xml/website_sale_product_recently_view.xml"],
    });
    publicWidget.registry.productsSearchBar.include({
        xmlDependencies: ["/website_rfq/static/src/xml/website_sale_product_search_view.xml"],
    });
});
