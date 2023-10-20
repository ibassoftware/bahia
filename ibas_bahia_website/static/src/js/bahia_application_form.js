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
			'click .add_record_books': '_onClickAdd_record_books',
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
				let relationship = $(row).find('select[id="relationship"]').val();
				let full_name = $(row).find('input[id="full_name"]').val();
				let applicant_gender = $(row).find('select[id="applicant_gender"]').val();
				let date_of_birth = $(row).find('input[id="date_of_birth"]').val();
				let placeof_birth = $(row).find('input[id="family_placeof_birth"]').val();
				console.log(relationship, full_name)
				family_data.push({
					'relationship': relationship,
					'full_name': full_name,
					'gender': applicant_gender,
					'date_of_birth': date_of_birth,
					'placeof_birth': placeof_birth
				});
			});
			$('textarea[name="applicant_families"]').val(JSON.stringify(family_data));

			// Education
			var education_rows = $('.applicant_education > tbody > tr.education_line');
			_.each(education_rows, function(row) {
				let schooltype = $(row).find('select[id="schooltype"]').val();
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

			// Record Books
			var record_books_rows = $('.applicant_record_books > tbody > tr.record_books_line');
			_.each(record_books_rows, function(row) {
				let document = $(row).find('select[id="document"]').val();
				let document_number = $(row).find('input[id="document_number"]').val();
				let date_issued = $(row).find('input[id="date_issued"]').val();
				let date_expiry = $(row).find('input[id="date_expiry"]').val();
				let issuing_authority = $(row).find('input[id="issuing_authority"]').val();
				let place_ofissue = $(row).find('input[id="place_ofissue"]').val();
				console.log(schooltype, name_school)
				record_books_data.push({
					'document': document,
					'document_number': document_number,
					'date_issued': date_issued,
					'date_expiry': date_expiry,
					'issuing_authority': issuing_authority,
					'place_ofissue': place_ofissue
				});
			});
			$('textarea[name="applicant_record_books"]').val(JSON.stringify(record_books_data));

			// Social Media
			var social_media_rows = $('.applicant_social_media > tbody > tr.social_media_line');
			_.each(social_media_rows, function(row) {
				let socialmedia_id = $(row).find('select[id="socialmedia_id"]').val();
				let name = $(row).find('input[id="name"]').val();
				console.log(socialmedia_id, name)
				social_media_data.push({
					'socialmedia_id': socialmedia_id,
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

		_onClickAdd_record_books: function(ev){
			console.log("add_record_books")
			var $new_row = $('.add_extra_record_books').clone(true);
			$new_row.removeClass('d-none');
			$new_row.removeClass('add_extra_record_books');
			$new_row.addClass('record_books_line');
			$new_row.insertBefore($('.add_extra_record_books'));
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