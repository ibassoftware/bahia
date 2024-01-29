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
			'click .add_employed_relative': '_onClickAdd_employed_relative',
			'click .add_previous_application': '_onClickAdd_previous_application',
			'click .add_previous_employment': '_onClickAdd_previous_employment',
			'click .add_social_media': '_onClickAdd_social_media',
			// 'click .remove_family_line': '_onClickRemove_family_line',
			'click .custom_create': '_onClickSubmit',
		},

		_onClickSubmit: async function(ev){
			console.log("submit application form")
			var self = this; 
			var family_data = [];
			var education_data = [];
			var record_books_data = [];
			var employed_relative_data = [];
			var previous_application_data = [];
			var previous_employment_data = [];
			var social_media_data = [];

			// Family
			var family_rows = $('.applicant_families > tbody > tr.family_line');
			_.each(family_rows, function(row) {
				let relationship = $(row).find('select[id="relationship"]').val();
				let first_name = $(row).find('input[id="first_name"]').val();
				let last_name = $(row).find('input[id="last_name"]').val();
				let applicant_gender = $(row).find('select[id="applicant_gender"]').val();
				let date_of_birth = $(row).find('input[id="date_of_birth"]').val();
				let placeof_birth = $(row).find('input[id="placeof_birth"]').val();
				family_data.push({
					'relationship': relationship,
					'first_name': first_name,
					'last_name': last_name,
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
			var record_books_rows = $('.applicant_document_ids > tbody > tr.record_books_line');
			_.each(record_books_rows, function(row) {
				let document = $(row).find('select[id="document"]').val();
				let document_number = $(row).find('input[id="document_number"]').val();
				let date_issued = $(row).find('input[id="date_issued"]').val();
				let date_expiry = $(row).find('input[id="date_expiry"]').val();
				let issuing_authority = $(row).find('input[id="issuing_authority"]').val();
				let place_ofissue = $(row).find('input[id="place_ofissue"]').val();
				record_books_data.push({
					'document': document,
					'document_number': document_number,
					'date_issued': date_issued,
					'date_expiry': date_expiry,
					'issuing_authority': issuing_authority,
					'place_ofissue': place_ofissue
				});
			});
			$('textarea[name="applicant_document_ids"]').val(JSON.stringify(record_books_data));

			// References - Employed Relatives
			var employed_relative_rows = $('.applicant_employed_relatives_ids > tbody > tr.employed_relative_line');
			_.each(employed_relative_rows, function(row) {
				let name_of_crew = $(row).find('input[id="name_of_crew"]').val();
				let position_and_principal = $(row).find('input[id="position_and_principal"]').val();
				let relationship = $(row).find('select[id="relationship"]').val();
				console.log(name_of_crew, position_and_principal)
				employed_relative_data.push({
					'name_of_crew': name_of_crew,
					'position_and_principal': position_and_principal,
					'relationship': relationship
				});
			});
			$('textarea[name="applicant_employed_relatives_ids"]').val(JSON.stringify(employed_relative_data));

			// References - Previous Application
			var previous_application_rows = $('.applicant_previous_application_ids > tbody > tr.previous_application_line');
			_.each(previous_application_rows, function(row) {
				let date_applied = $(row).find('input[id="date_applied"]').val();
				let job_applied_id = $(row).find('select[id="job_applied_id"]').val();
				console.log(date_applied, job_applied_id)
				previous_application_data.push({
					'date_applied': date_applied,
					'job_applied_id': job_applied_id
				});
			});
			$('textarea[name="applicant_previous_application_ids"]').val(JSON.stringify(previous_application_data));

			// References - Previous Employment
			var previous_employment_rows = $('.applicant_previous_employment_ids > tbody > tr.previous_employment_line');
			_.each(previous_employment_rows, function(row) {
				let rank_position = $(row).find('input[id="rank_position"]').val();
				let manning_agency = $(row).find('input[id="manning_agency"]').val();
				let employer_principal = $(row).find('input[id="employer_principal"]').val();
				let address_contact_info_manning_agen = $(row).find('input[id="address_contact_info_manning_agen"]').val();
				let vessel_name = $(row).find('input[id="vessel_name"]').val();
				let vessel_type = $(row).find('select[id="vessel_type"]').val();
				let grt = $(row).find('input[id="grt"]').val();
				let date_from = $(row).find('input[id="date_from"]').val();
				let date_to = $(row).find('input[id="date_to"]').val();
				let duties_and_responsibility = $(row).find('input[id="duties_and_responsibility"]').val();
				previous_employment_data.push({
					'rank_position': rank_position,
					'manning_agency': manning_agency,
					'employer_principal': employer_principal,
					'address_contact_info_manning_agen': address_contact_info_manning_agen,
					'vessel_name': vessel_name,
					'vessel_type': vessel_type,
					'grt': grt,
					'date_from': date_from,
					'date_to': date_to,
					'duties_and_responsibility': duties_and_responsibility
				});
			});
			$('textarea[name="applicant_previous_employment_ids"]').val(JSON.stringify(previous_employment_data));

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

		// _onClickRemove_family_line: function(ev){
		// 	console.log("remove_family")
		// 	$(this).parent().parent().remove();
		// },

		_onClickAdd_family: function(ev){
			console.log("add_family")
			var $new_row = $('.add_extra_family').clone(true);
			$new_row.removeClass('d-none');
			$new_row.removeClass('add_extra_family');
			$new_row.addClass('family_line');
			$new_row.insertBefore($('.add_extra_family'));
			_.each($new_row.find('td'), function(val) {
				$(val).find('select').attr('required', '');
				$(val).find('input').attr('required', '');
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

		_onClickAdd_employed_relative: function(ev){
			console.log("add_employed_relative")
			var $new_row = $('.add_extra_employed_relative').clone(true);
			$new_row.removeClass('d-none');
			$new_row.removeClass('add_extra_employed_relative');
			$new_row.addClass('employed_relative_line');
			$new_row.insertBefore($('.add_extra_employed_relative'));
			_.each($new_row.find('td'), function(val) {
				$(val).find('input').attr('required', 'required');
			});
		},

		_onClickAdd_previous_application: function(ev){
			console.log("add_previous_application")
			var $new_row = $('.add_extra_previous_application').clone(true);
			$new_row.removeClass('d-none');
			$new_row.removeClass('add_extra_previous_application');
			$new_row.addClass('previous_application_line');
			$new_row.insertBefore($('.add_extra_previous_application'));
			_.each($new_row.find('td'), function(val) {
				$(val).find('input').attr('required', 'required');
			});
		},

		_onClickAdd_previous_employment: function(ev){
			console.log("add_previous_employment")
			var $new_row = $('.add_extra_previous_employment').clone(true);
			$new_row.removeClass('d-none');
			$new_row.removeClass('add_extra_previous_employment');
			$new_row.addClass('previous_employment_line');
			$new_row.insertBefore($('.add_extra_previous_employment'));
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