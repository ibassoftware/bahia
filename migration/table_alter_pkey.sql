-- Fix missing primary keys
ALTER TABLE hr_department ADD PRIMARY KEY (id);
ALTER TABLE res_users ADD PRIMARY KEY (id);
ALTER TABLE hr_religion ADD PRIMARY KEY (id);
ALTER TABLE resource_resource ADD PRIMARY KEY (id);
ALTER TABLE hr_employee ADD PRIMARY KEY (id);
ALTER TABLE res_partner ADD PRIMARY KEY (id);
ALTER TABLE hr_job ADD PRIMARY KEY (id);
ALTER TABLE res_country ADD PRIMARY KEY (id);
ALTER TABLE res_partner_bank ADD PRIMARY KEY (id);

ALTER TABLE hr_licensetype ADD PRIMARY KEY (id);
ALTER TABLE hr_vesselcategory ADD PRIMARY KEY (id);
ALTER TABLE hr_companies ADD PRIMARY KEY (id);
ALTER TABLE hr_ranktype ADD PRIMARY KEY (id);
ALTER TABLE hr_documenttype ADD PRIMARY KEY (id);
ALTER TABLE hr_license ADD PRIMARY KEY (id);
ALTER TABLE hr_medicalrecord ADD PRIMARY KEY (id);
ALTER TABLE hr_checklist ADD PRIMARY KEY (id);
ALTER TABLE hr_addresstype ADD PRIMARY KEY (id);
ALTER TABLE hr_recruitment_degree ADD PRIMARY KEY (id);
ALTER TABLE hr_familyrelations ADD PRIMARY KEY (id);
ALTER TABLE hr_clinic ADD PRIMARY KEY (id);
ALTER TABLE hr_rank ADD PRIMARY KEY (id);
ALTER TABLE hr_employment_status ADD PRIMARY KEY (id);
ALTER TABLE hr_port ADD PRIMARY KEY (id);
ALTER TABLE hr_ship_department ADD PRIMARY KEY (id);
ALTER TABLE hr_vessel ADD PRIMARY KEY (id);
ALTER TABLE hr_checklist_template ADD PRIMARY KEY (id);
ALTER TABLE hr_employee_checklist_documents ADD PRIMARY KEY (id);
ALTER TABLE hr_personnel_withrmks_main ADD PRIMARY KEY (id);
ALTER TABLE hr_disembarkation_main ADD PRIMARY KEY (id);
ALTER TABLE hr_embarkation_main ADD PRIMARY KEY (id);
ALTER TABLE hr_signonoff_report_main ADD PRIMARY KEY (id);
ALTER TABLE hr_personnel_withrelative_main ADD PRIMARY KEY (id);
ALTER TABLE ir_model ADD PRIMARY KEY (id);
ALTER TABLE ir_model_fields ADD PRIMARY KEY (id);
ALTER TABLE hr_applicant ADD PRIMARY KEY (id);
ALTER TABLE hr_applicant_evaluation ADD PRIMARY KEY (id);
ALTER TABLE hr_recruitment_stage ADD PRIMARY KEY (id);
ALTER TABLE survey_user_input ADD PRIMARY KEY (id);
ALTER TABLE res_company ADD PRIMARY KEY (id);
ALTER TABLE hr_recruitment_source ADD PRIMARY KEY (id);
ALTER TABLE hr_checklist_template_main ADD PRIMARY KEY (id);
ALTER TABLE res_groups ADD PRIMARY KEY (id);
ALTER TABLE mail_alias ADD PRIMARY KEY (id);
ALTER TABLE ir_ui_menu ADD PRIMARY KEY (id);

-- Fix foreign key references for missing job ids
SELECT count(id) FROM hr_employee where job_id='219';
UPDATE hr_employee SET job_id=NULL where job_id='219';

SELECT count(id) FROM hr_employee where job_id='203';
UPDATE hr_employee SET job_id=NULL where job_id='203';

SELECT count(id) FROM hr_employee where job_id='337';
UPDATE hr_employee SET job_id=NULL where job_id='337';

SELECT count(id) FROM hr_employee where job_id='473';
UPDATE hr_employee SET job_id=NULL where job_id='473';

SELECT count(id) FROM hr_employee where job_id='474';
UPDATE hr_employee SET job_id=NULL where job_id='474';

SELECT count(id) FROM hr_employee where job_id='447';
UPDATE hr_employee SET job_id=NULL where job_id='447';

SELECT count(id) FROM hr_employee where job_id='234';
UPDATE hr_employee SET job_id=NULL where job_id='234';

-- Fix foreign key references for missing job id in hr evaluation
SELECT count(id) FROM hr_applicant_evaluation where job_approved_id='219';
UPDATE hr_applicant_evaluation SET job_approved_id=NULL where job_approved_id='219';

SELECT count(id) FROM hr_applicant_evaluation where job_approved_id='203';
UPDATE hr_applicant_evaluation SET job_approved_id=NULL where job_approved_id='203';

SELECT count(id) FROM hr_applicant_evaluation where job_approved_id='447';
UPDATE hr_applicant_evaluation SET job_approved_id=NULL where job_approved_id='447';

SELECT count(id) FROM hr_applicant_evaluation where job_approved_id='464';
UPDATE hr_applicant_evaluation SET job_approved_id=NULL where job_approved_id='464';

SELECT count(id) FROM hr_applicant_evaluation where job_applied_id='219';
UPDATE hr_applicant_evaluation SET job_applied_id=NULL where job_applied_id='219';

SELECT count(id) FROM hr_applicant_evaluation where job_applied_id='203';
UPDATE hr_applicant_evaluation SET job_applied_id=NULL where job_applied_id='203';

SELECT count(id) FROM hr_applicant_evaluation where job_applied_id='447';
UPDATE hr_applicant_evaluation SET job_applied_id=NULL where job_applied_id='447';

SELECT count(id) FROM hr_applicant_evaluation where job_applied_id='464';
UPDATE hr_applicant_evaluation SET job_applied_id=NULL where job_applied_id='464';

SELECT count(id) FROM hr_applicant_evaluation where job_applied_id='474';
UPDATE hr_applicant_evaluation SET job_applied_id=NULL where job_applied_id='474';

SELECT count(id) FROM hr_applicant_evaluation where job_applied_id='473';
UPDATE hr_applicant_evaluation SET job_applied_id=NULL where job_applied_id='473';

SELECT count(id) FROM hr_applicant_evaluation where job_applied_id='448';
UPDATE hr_applicant_evaluation SET job_applied_id=NULL where job_applied_id='448';

-- Fix foreign key references for missing vessel in hr_employee_checklist_documents
SELECT count(id) FROM hr_employee_checklist_documents where vessel_id='424';
UPDATE hr_employee_checklist_documents SET vessel_id=NULL where vessel_id='424';