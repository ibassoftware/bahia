--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: hr_medicalrecord; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (13, 1, '100', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'NationalHealth Cert');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (14, 1, '140', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'YellowFever Vaccination');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (15, 1, '3', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'Yellow Fever - Allergic Reaction');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (16, 1, '150', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'AlcoholTest');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (17, 1, '160', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'Drug Test');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (18, 1, '161', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'HIV Screening Test');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (19, 1, '110', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'X-Ray');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (20, 1, '162', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'Hepa A Vacc');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (21, 1, '163', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'Hepa B Vacc');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (22, 1, '164', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'Hep B inactive carrier');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (23, 1, '165', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'Cervical Vaccination');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (24, 1, '168', '2016-09-12 10:41:01.480892', NULL, 1, '2016-09-12 10:41:01.480892', 'Typhoid');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (44, 30065, 'Hepa A Vacc 2nd Dose', '2017-10-18 02:41:12.799947', NULL, 30065, '2017-10-18 02:41:12.799947', 'Hepa A Vacc 2nd Dose');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (57, 30065, 'Hepa B Booster', '2019-09-10 05:57:12.198951', NULL, 30065, '2019-09-10 05:57:12.198951', 'Hepa B Booster');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (66, 1, 'PCR Test', '2021-04-26 22:59:52.063361', 'Swab Test prior crew departure', 1, '2021-04-26 22:59:52.063361', 'Swab Test');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (67, 1, 'RT PCR 24Hrs', '2021-04-27 23:42:23.614003', NULL, 1, '2021-04-27 23:42:23.614003', 'RT PCR 24Hrs');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (68, 1, 'RT PCR 48Hrs', '2021-04-27 23:42:41.93997', NULL, 1, '2021-04-27 23:42:41.93997', 'RT PCR 48Hrs');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (69, 1, 'RT PCR 72Hrs', '2021-04-27 23:48:27.672701', NULL, 1, '2021-04-27 23:48:27.672701', 'RT PCR 72Hrs');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (75, 30065, 'Covid vacc', '2021-08-25 02:53:49.681683', NULL, 30065, '2021-08-25 02:53:49.681683', 'Covid vacc - Janssen');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (77, 30065, 'Covid Vaccination', '2021-08-25 02:54:23.001207', NULL, 30065, '2021-08-25 02:54:23.001207', 'Covid Vaccination');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (79, 30065, 'Covid Vaccination 1st. dose', '2021-08-31 23:43:16.244127', NULL, 30065, '2021-08-31 23:43:16.244127', 'Covid Vaccination 1st. dose');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (81, 30065, 'Covid Vaccination 2nd. dose', '2021-08-31 23:44:07.111966', NULL, 30065, '2021-08-31 23:44:07.111966', 'Covid Vaccination 2nd. dose');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (84, 30047, '207', '2021-10-26 23:54:07.535149', NULL, 30047, '2021-10-26 23:54:07.535149', 'ICV');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (86, 30047, '208', '2021-11-10 06:08:48.94204', NULL, 30047, '2021-11-10 06:08:48.94204', 'PFIZER');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (88, 30065, 'National Health Certificate', '2021-12-10 00:22:00.487942', NULL, 30065, '2021-12-10 00:22:00.487942', 'National Health Cert');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (90, 30065, 'National Health Certificate', '2021-12-10 02:03:14.841148', NULL, 30065, '2021-12-10 02:03:14.841148', 'National Health Cert');
INSERT INTO hr_medicalrecord (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (92, 30065, 'Covid Booster ', '2022-03-07 03:08:31.925887', NULL, 30065, '2022-03-07 03:08:31.925887', 'Covid Booster');


--
-- Name: hr_medicalrecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_medicalrecord_id_seq', 92, true);


--
-- PostgreSQL database dump complete
--

