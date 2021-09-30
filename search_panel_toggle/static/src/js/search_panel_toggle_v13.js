odoo.define('search_panel_toggle.SPanel',function (require) {
"use strict";

/**
 * 1.扩展search panel,使其在能够工作下搜索对话框中．
 */
	var ListView = require("web.ListView");
	var ListController = require("web.ListController");
	var SearchPanel = require('web.SearchPanel');
	var Dialog = require("web.Dialog");
	var ViewDialog = require("web.view_dialogs");
	var core = require("web.core");
	var pyeval=require("web.py_utils");
	var viewUtils = require('web.viewUtils');
	var QWeb = core.qweb;																		
	var _t = core._t;
									 
	SearchPanel.include({
	    /**
	     * 增加toggle按钮，处理SearchPanel的显示和隐藏
	     */
	    on_attach_callback: function () {

	       var self = this;
	   
		   this._super.apply(this,arguments);
				   
		   var $el = this.$el;
		   var  $toggleButton = $el.siblings('button.btn-search-panel-toggle');
			if($toggleButton.length){
				return;
			}
	       var $hideButton = QWeb.render("SearchPanel.HideButton",this);
	       var $buttonEl = $(document.createDocumentFragment());
	       $buttonEl.append($hideButton);	       	       
	       $buttonEl.find('button.btn-search-panel-toggle').click(function(){
				 if(self.$el.hasClass('o_hidden')){
					 self.do_show();
					 $(this).removeClass('fa-caret-right show-panel').addClass('fa-caret-left hide-panel');;
				 }else{
					 self.do_hide();
					 $(this).addClass('fa-caret-right show-panel').removeClass('fa-caret-left hide-panel');
				 }
			 }); 
	       this.$el.after($buttonEl);
	    },
	
	});
 
});
