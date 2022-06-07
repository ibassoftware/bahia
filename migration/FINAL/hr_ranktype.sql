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
-- Data for Name: hr_ranktype; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (9, 1, 'J', '2016-09-12 10:55:56.049094', 'Jr. Officer', 1, 75.00, '2016-09-12 10:55:56.049094', 'Jr. Officer');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (10, 1, 'O', '2016-09-12 10:55:56.049094', 'Officer', 1, 75.00, '2016-09-12 10:55:56.049094', 'Officer');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (11, 1, 'R', '2016-09-12 10:55:56.049094', 'Rating', 1, 30.00, '2016-09-12 10:55:56.049094', 'Rating');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (12, 1, 'C', '2016-09-12 10:55:56.049094', 'Catering', 1, 75.00, '2016-09-12 10:55:56.049094', 'Catering');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (13, 1, 'HO', '2016-09-12 10:55:56.049094', 'Hotel-Officer', 1, 65.00, '2016-09-12 10:55:56.049094', 'Hotel-Officer');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (14, 1, 'CR', '2016-09-12 10:55:56.049094', 'Catering-Rating', 1, 10.00, '2016-09-12 10:55:56.049094', 'Catering-Rating');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (15, 1, 'HR', '2016-09-12 10:55:56.049094', 'Hotel-Rating', 1, 15.00, '2016-09-12 10:55:56.049094', 'Hotel-Rating');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (16, 1, 'CO', '2016-09-12 10:55:56.049094', 'Catering-Officer', 1, 55.00, '2016-09-12 10:55:56.049094', 'Catering-Officer');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (21, 30065, 'OFFSHORE TANKER', '2017-01-13 01:19:08.878567', NULL, 30065, 0.00, '2017-01-13 01:19:08.878567', '3/E');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (24, 30065, '10008', '2017-05-22 03:20:01.542084', NULL, 30065, 0.00, '2017-05-22 03:20:01.542084', 'Jr. Officer');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (28, 30065, '20000', '2019-05-15 08:03:07.295304', NULL, 30065, 0.00, '2019-05-15 08:03:07.295304', 'Ftr');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (32, 30067, '012231', '2019-06-26 06:54:22.751524', NULL, 30067, 0.00, '2019-06-26 06:54:22.751524', 'Ratings');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (35, 30067, '444175', '2019-08-06 08:59:32.85881', 'Supervisor', 30067, 0.00, '2019-08-06 08:59:32.85881', 'Supervisor');
INSERT INTO hr_ranktype (id, create_uid, code, create_date, description, write_uid, rate, write_date, name) VALUES (37, 1, 'RO', '2020-10-23 01:25:09.957593', NULL, 1, 0.00, '2020-10-23 01:25:09.957593', 'Recycling Operative');


--
-- Name: hr_ranktype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_ranktype_id_seq', 37, true);


--
-- PostgreSQL database dump complete
--

