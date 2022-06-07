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
-- Data for Name: hr_department; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (1, 1, '2016-09-23 03:52:54.757525', 'DECK DEPARTMENT', 1, 1, NULL, NULL, NULL, '2016-09-23 03:52:54.757525');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (2, 30049, '2016-09-28 05:33:19.443503', 'HOUSEKEEPING', 1, 30049, NULL, NULL, NULL, '2016-09-28 05:33:19.443503');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (3, 30065, '2016-10-06 07:34:35.514842', 'CATERING DEPARTMENT', 1, 30065, NULL, NULL, NULL, '2016-10-06 07:34:35.514842');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (4, 30065, '2016-10-06 23:17:20.441304', 'ENGINE DEPARTMENT', 1, 30065, NULL, NULL, NULL, '2016-10-06 23:17:20.441304');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (5, 30067, '2016-10-07 00:33:04.924732', 'HOTEL DEPARTMENT', 1, 30067, NULL, NULL, NULL, '2016-10-07 00:34:40.301229');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (6, 30067, '2016-10-07 00:35:28.737663', 'HOUSEKEEPING DEPARTMENT', 1, 30067, NULL, NULL, NULL, '2016-10-07 00:35:28.737663');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (7, 30067, '2016-10-07 00:40:41.241985', 'ENTERTAINMENT', 1, 30067, NULL, NULL, NULL, '2016-10-07 00:40:41.241985');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (8, 30050, '2016-10-11 03:20:48.790313', 'CARNIVAL CRUISE LINES', 1, 30050, NULL, NULL, NULL, '2016-10-11 03:20:48.790313');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (9, 1, '2016-11-15 00:29:42.549984', 'DECK NON PAX', 1, 1, NULL, NULL, NULL, '2016-11-15 00:29:42.549984');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (10, 1, '2016-11-15 00:29:58.12195', 'ENGINE NON PAX', 1, 1, NULL, NULL, NULL, '2016-11-15 00:29:58.12195');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (11, 30050, '2016-12-09 07:42:47.663196', 'DECK ADMIN JR ', 1, 30050, NULL, NULL, NULL, '2016-12-09 07:42:47.663196');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (12, 30047, '2017-01-21 03:11:18.031584', 'GALLEY', 1, 30047, NULL, NULL, NULL, '2017-01-21 03:11:18.031584');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (13, 30067, '2018-06-21 01:35:49.288718', 'Chief Security Officer', 1, 30067, NULL, NULL, NULL, '2018-06-21 01:35:49.288718');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (14, 30078, '2018-07-06 03:29:02.538945', 'Culinary', 1, 30078, NULL, NULL, NULL, '2018-07-06 03:29:02.538945');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (15, 30078, '2019-05-16 03:11:04.245661', 'galley', 1, 30078, NULL, NULL, NULL, '2019-05-16 03:11:04.245661');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (16, 30078, '2021-07-01 08:30:26.238661', 'Restaurant', 1, 30078, NULL, NULL, NULL, '2021-07-01 08:30:26.238661');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (17, 30078, '2021-07-02 05:29:39.608439', 'BAR', 1, 30078, NULL, NULL, NULL, '2021-07-02 05:29:39.608439');
INSERT INTO hr_department (id, create_uid, create_date, name, company_id, write_uid, note, parent_id, manager_id, write_date) VALUES (18, 30047, '2021-07-27 05:30:49.126257', 'STAGE MANAGER', 1, 30047, NULL, NULL, NULL, '2021-07-27 05:30:49.126257');


--
-- Name: hr_department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_department_id_seq', 18, true);


--
-- PostgreSQL database dump complete
--

