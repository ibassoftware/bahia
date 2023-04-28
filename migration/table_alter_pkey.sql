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

-- Fix foreing key references for missing job ids
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