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
-- Data for Name: hr_employment_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (21, 1, '2016-09-12 10:56:46.287996', 'Active on board', 'ACT', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (22, 1, '2016-09-12 10:56:46.287996', 'Inactive', 'INA', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (23, 1, '2016-09-12 10:56:46.287996', 'Available', 'AVA', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (24, 1, '2016-09-12 10:56:46.287996', 'No rehire', 'NRH', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (25, 1, '2016-09-12 10:56:46.287996', 'Office visit', 'OFF', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (26, 1, '2016-09-12 10:56:46.287996', 'Office work', 'OFW', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (27, 1, '2016-09-12 10:56:46.287996', 'Retired', 'RET', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (28, 1, '2016-09-12 10:56:46.287996', 'Sick leave, active', 'SCK', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (30, 1, '2016-09-12 10:56:46.287996', 'Stand by', 'STB', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (31, 1, '2016-09-12 10:56:46.287996', 'Start up', 'STP', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (32, 1, '2016-09-12 10:56:46.287996', 'Transferred', 'TRF', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (33, 1, '2016-09-12 10:56:46.287996', 'Travelling day(s)', 'TVL', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (34, 1, '2016-09-12 10:56:46.287996', 'Vacation', 'VAC', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (35, 1, '2016-09-12 10:56:46.287996', 'Travelling on board', 'TVO', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (36, 1, '2016-09-12 10:56:46.287996', 'Course', 'CRS', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (37, 1, '2016-09-12 10:56:46.287996', 'Officer conference', 'OFC', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (38, 1, '2016-09-12 10:56:46.287996', 'Sick leave', 'SIC', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (39, 1, '2016-09-12 10:56:46.287996', 'Compassionate Leave', 'CL', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (40, 1, '2016-09-12 10:56:46.287996', 'Leave', 'LVE', 1, '2016-09-12 10:56:46.287996');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (41, 1, '2016-09-18 11:38:56.524621', 'Dismissed', 'Dismissed', 1, '2016-09-18 11:47:06.444912');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (42, 1, '2016-09-22 07:01:02.080384', 'Travelling Between Ships', 'Travelling Between Ships', 1, '2016-09-22 07:01:02.080384');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (43, 30050, '2016-11-08 06:25:49.733976', 'Lead Nurse', NULL, 30050, '2016-11-08 06:25:49.733976');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (44, 30050, '2016-11-29 07:44:19.10601', 'Env''l Team Member - Level A', NULL, 30050, '2016-11-29 07:44:19.10601');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (45, 1, '2016-12-08 03:24:13.144888', 'No Return from Vacation', 'No Return from Vacation', 1, '2016-12-08 03:24:13.144888');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (46, 1, '2016-12-08 05:39:22.248646', 'NO RETURN FROM VACATION (1st Contract)', 'NO RETURN FROM VACATION (1st Contract)', 1, '2016-12-08 05:39:22.248646');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (47, 1, '2017-01-09 05:28:36.482537', 'FINISHED CONTRACT', 'FINISHED CONTRACT', 1, '2017-01-09 05:28:36.482537');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (48, 30049, '2017-01-09 05:53:29.277892', 'Resigned', NULL, 30049, '2017-01-09 05:53:29.277892');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (49, 30049, '2017-01-09 06:33:28.982031', 'FINISHED', NULL, 30049, '2017-01-09 06:33:28.982031');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (50, 30049, '2017-01-16 00:06:25.581045', 'LEVEL C', NULL, 30049, '2017-01-16 00:06:25.581045');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (51, 30070, '2017-01-25 02:21:07.225513', 'SICKE LEAVE', NULL, 30070, '2017-01-25 02:21:07.225513');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (29, 1, '2016-09-12 10:56:46.287996', 'Sick leave/Medically Unfit', 'SCL', 1, '2017-02-27 06:41:48.21823');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (52, 30070, '2017-02-28 02:56:39.662793', 'actove', NULL, 30070, '2017-02-28 02:56:39.662793');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (53, 30070, '2017-03-06 05:41:40.039713', 'ACTVE', NULL, 30070, '2017-03-06 05:41:40.039713');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (54, 30048, '2017-03-15 00:51:34.310944', 'on treatment until july.2017', NULL, 30048, '2017-03-15 00:51:34.310944');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (55, 30070, '2017-03-21 02:29:47.111773', 'ACTIVE', NULL, 30070, '2017-03-21 02:29:47.111773');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (56, 30070, '2017-03-21 02:30:07.753514', 'ACTIVE', NULL, 30070, '2017-03-21 02:30:07.753514');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (57, 30070, '2017-03-27 23:38:59.143144', 'ACTIVE ', NULL, 30070, '2017-03-27 23:38:59.143144');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (58, 30048, '2017-04-02 23:52:53.910947', 'SICKNESS', NULL, 30048, '2017-04-02 23:52:53.910947');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (59, 30057, '2017-04-06 02:27:58.256297', 'Active on board', NULL, 30057, '2017-04-06 02:27:58.256297');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (60, 30070, '2017-04-06 05:30:58.443563', 'ACTIV EON ', NULL, 30070, '2017-04-06 05:30:58.443563');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (61, 30070, '2017-05-28 23:48:48.836296', 'ACITVE ', NULL, 30070, '2017-05-28 23:48:48.836296');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (63, 30049, '2017-08-07 00:49:44.979313', 'Active on board', NULL, 30049, '2017-08-07 00:49:44.979313');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (65, 30049, '2017-09-05 01:26:40.072575', 'TERMINATION', NULL, 30049, '2017-09-05 01:26:40.072575');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (62, 30067, '2017-06-13 06:14:20.167194', 'WITHDRAW', 'WITHDRAW', 1, '2017-10-10 00:41:23.622227');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (66, 30049, '2017-11-06 01:58:51.045946', 'Active on board', NULL, 30049, '2017-11-06 01:58:51.045946');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (67, 31152, '2018-05-16 06:20:37.424172', 'TERMINATE', NULL, 31152, '2018-05-16 06:20:37.424172');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (68, 31152, '2018-07-09 03:35:31.531448', 'RESIGND', NULL, 31152, '2018-07-09 03:35:31.531448');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (69, 30067, '2018-08-22 02:40:58.934585', 'No Rehire', NULL, 30067, '2018-08-22 02:40:58.934585');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (70, 30049, '2018-09-25 03:07:46.815137', 'INC', NULL, 30049, '2018-09-25 03:07:46.815137');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (77, 30067, '2019-07-11 03:27:16.641284', 'Decease', '9874', 30067, '2019-07-11 03:27:31.621643');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (78, 30049, '2019-08-13 06:34:35.368069', 'black', NULL, 30049, '2019-08-13 06:34:35.368069');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (79, 30068, '2019-10-03 07:24:26.601796', 'inactive', NULL, 30068, '2019-10-03 07:24:26.601796');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (80, 1, '2020-01-30 02:32:32.731141', '2 YRS VALIDITY', 'OWWA VALIDITY', 1, '2020-01-30 02:32:32.731141');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (81, 1, '2020-01-30 02:33:13.895604', 'OWWA  VALIDITY', 'OWWA', 1, '2020-01-30 02:33:13.895604');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (82, 30051, '2020-01-30 08:31:02.946894', 'owwa ', NULL, 30051, '2020-01-30 08:31:02.946894');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (83, 30049, '2020-02-10 05:41:05.642712', 'AC', NULL, 30049, '2020-02-10 05:41:05.642712');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (84, 30049, '2020-02-21 05:25:18.521471', 'ac', NULL, 30049, '2020-02-21 05:25:18.521471');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (85, 30049, '2020-03-25 04:03:56.047634', 'AVA', NULL, 30049, '2020-03-25 04:03:56.047634');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (86, 30049, '2020-04-02 06:00:48.96033', 'AVA', NULL, 30049, '2020-04-02 06:00:48.96033');
INSERT INTO hr_employment_status (id, create_uid, create_date, name, status_id, write_uid, write_date) VALUES (87, 30047, '2021-02-15 02:49:52.210712', 'maternity leave', NULL, 30047, '2021-02-15 02:49:52.210712');


--
-- Name: hr_employment_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_employment_status_id_seq', 87, true);


--
-- PostgreSQL database dump complete
--

