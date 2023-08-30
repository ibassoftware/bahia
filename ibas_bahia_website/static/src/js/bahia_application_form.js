odoo.define('ibas_bahia_website.apply_template', function(require){
	"use strict";
	var publicWidget = require('web.public.widget');
	var core = require('web.core');
	var ajax = require('web.ajax');
	var rpc = require('web.rpc');
	var core = require('web.core');
	var QWeb = core.qweb;
	var _t = core._t;

	publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
		selector: '#apply_template',
		events: {
		'click .add_family': '_onClickAdd_family',
		'click .remove_family_line': '_onClickRemove_family_line',
		//'click .custom_create': '_onClickSubmit',
	},

	// _onClickSubmit: async function(ev){
	// 	var self = this; 
	// 	var cost_data = [];
	// 	var rows = $('.total_project_costs > tbody > tr.project_cost_line');
	// 	_.each(rows, function(row) {
	// 		let expenditure = $(row).find('input[name="expenditure"]').val();
	// 		let total_cost = $(row).find('input[name="total_cost"]').val();
	// 		console.log(expenditure, total_cost)
	// 		cost_data.push({
	// 			'code': expenditure,
	// 			'cost': total_cost,
	// 		});
	// 	});
	// 	$('textarea[name="data_family_line_ids"]').val(JSON.stringify(cost_data));

	// },

	_onClickRemove_family_line: function(ev){
		$(this).parent().parent().remove();
	},

	_onClickAdd_family: function(ev){
		console.log("add_family")
		var $new_row = $('.add_extra_family').clone(true);
		$new_row.removeClass('d-none');
		$new_row.removeClass('add_extra_family');
		$new_row.addClass('family_line');
		$new_row.insertBefore($('.add_extra_family'));
		_.each($new_row.find('td'), function(val) {
			$(val).find('input').attr('required', 'required');
		});
	},

	});
});