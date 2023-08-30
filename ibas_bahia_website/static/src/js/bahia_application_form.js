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
		selector: '#application_form_template',
		events: {
			'click .add_family': '_onClickAdd_family',
			'click .add_education': '_onClickAdd_education',
			'click .add_social_media': '_onClickAdd_social_media',
			'click .remove_family_line': '_onClickRemove_family_line',
			'click .custom_create': '_onClickSubmit',
		},

		_onClickSubmit: async function(ev){
			var self = this; 
			var family_data = [];
			var education_data = [];
			var social_media_data = [];

			// Family
			var family_rows = $('.applicant_families > tbody > tr.family_line');
			_.each(family_rows, function(row) {
				let relationship = $(row).find('input[id="relationship"]').val();
				let full_name = $(row).find('input[id="full_name"]').val();
				let applicant_gender = $(row).find('input[id="applicant_gender"]').val();
				let date_of_birth = $(row).find('input[id="date_of_birth"]').val();
				let placeof_birth = $(row).find('input[id="family_placeof_birth"]').val();
				console.log(relationship, full_name)
				family_data.push({
					'relationship': relationship,
					'full_name': full_name,
					'applicant_gender': applicant_gender,
					'date_of_birth': date_of_birth,
					'placeof_birth': placeof_birth
				});
			});
			$('textarea[name="applicant_families"]').val(JSON.stringify(family_data));

			// Education
			var education_rows = $('.applicant_education > tbody > tr.education_line');
			_.each(education_rows, function(row) {
				let schooltype = $(row).find('input[id="schooltype"]').val();
				let name_school = $(row).find('input[id="name_school"]').val();
				let description = $(row).find('input[id="description"]').val();
				let date_from = $(row).find('input[id="date_from"]').val();
				let date_to = $(row).find('input[id="date_to"]').val();
				let school_address = $(row).find('input[id="school_address"]').val();
				console.log(schooltype, name_school)
				education_data.push({
					'schooltype': schooltype,
					'name_school': name_school,
					'description': description,
					'date_from': date_from,
					'date_to': date_to,
					'school_address': school_address
				});
			});
			$('textarea[name="applicant_education"]').val(JSON.stringify(education_data));

			// Social Media
			var social_media_rows = $('.applicant_social_media > tbody > tr.social_media_line');
			_.each(social_media_rows, function(row) {
				let socialmedia_ids = $(row).find('input[id="socialmedia_ids"]').val();
				let name = $(row).find('input[id="name"]').val();
				console.log(socialmedia_ids, name)
				social_media_data.push({
					'socialmedia_ids': socialmedia_ids,
					'name': name,
				});
			});
			$('textarea[name="applicant_socialmedia_ids"]').val(JSON.stringify(social_media_data));

		},

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

		_onClickAdd_education: function(ev){
			console.log("add_education")
			var $new_row = $('.add_extra_education').clone(true);
			$new_row.removeClass('d-none');
			$new_row.removeClass('add_extra_education');
			$new_row.addClass('education_line');
			$new_row.insertBefore($('.add_extra_education'));
			_.each($new_row.find('td'), function(val) {
				$(val).find('input').attr('required', 'required');
			});
		},

		_onClickAdd_social_media: function(ev){
			console.log("add_social_media")
			var $new_row = $('.add_extra_social_media').clone(true);
			$new_row.removeClass('d-none');
			$new_row.removeClass('add_extra_social_media');
			$new_row.addClass('social_media_line');
			$new_row.insertBefore($('.add_extra_social_media'));
			_.each($new_row.find('td'), function(val) {
				$(val).find('input').attr('required', 'required');
			});
		},

	});
});