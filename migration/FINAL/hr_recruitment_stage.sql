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
-- Data for Name: hr_recruitment_stage; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_recruitment_stage (id, create_uid, requirements, name, sequence, write_uid, fold, write_date, create_date, template_id, department_id, legend_normal, legend_blocked, legend_done) VALUES (3, 1, NULL, 'Reserved (Pooling)', 2, 30067, false, '2016-11-11 02:24:17.566624', '2016-09-12 10:33:32.720694', NULL, NULL, 'In Progress', 'Blocked', 'Ready for Next Stage');
INSERT INTO hr_recruitment_stage (id, create_uid, requirements, name, sequence, write_uid, fold, write_date, create_date, template_id, department_id, legend_normal, legend_blocked, legend_done) VALUES (1, 1, NULL, 'Initial Qualification (Screening)', 1, 30067, false, '2016-11-11 02:24:39.364589', '2016-09-12 10:33:32.720694', 10, NULL, 'In Progress', 'Blocked', 'Ready for Next Stage');
INSERT INTO hr_recruitment_stage (id, create_uid, requirements, name, sequence, write_uid, fold, write_date, create_date, template_id, department_id, legend_normal, legend_blocked, legend_done) VALUES (2, 1, NULL, 'Qualified/Passed', 3, 1, false, '2018-06-11 18:43:52.235418', '2016-09-12 10:33:32.720694', 9, NULL, 'In Progress', 'Blocked', 'Ready for Next Stage');
INSERT INTO hr_recruitment_stage (id, create_uid, requirements, name, sequence, write_uid, fold, write_date, create_date, template_id, department_id, legend_normal, legend_blocked, legend_done) VALUES (6, 1, NULL, 'Reject', 4, 1, false, '2018-06-11 18:44:17.124007', '2016-09-12 10:33:32.720694', 8, NULL, 'In Progress', 'Blocked', 'Ready for Next Stage');
INSERT INTO hr_recruitment_stage (id, create_uid, requirements, name, sequence, write_uid, fold, write_date, create_date, template_id, department_id, legend_normal, legend_blocked, legend_done) VALUES (4, 1, NULL, 'Contract Proposed (Endorsed Candidates)', 6, 1, true, '2018-06-11 18:44:17.125034', '2016-09-12 10:33:32.720694', NULL, NULL, 'In Progress', 'Blocked', 'Ready for Next Stage');
INSERT INTO hr_recruitment_stage (id, create_uid, requirements, name, sequence, write_uid, fold, write_date, create_date, template_id, department_id, legend_normal, legend_blocked, legend_done) VALUES (5, 1, NULL, 'Contract Signed (Processed Candidates)', 6, 1, true, '2018-06-11 18:44:25.437043', '2016-09-12 10:33:32.720694', NULL, NULL, 'In Progress', 'Blocked', 'Ready for Next Stage');


--
-- Name: hr_recruitment_stage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_recruitment_stage_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--

