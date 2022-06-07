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
-- Data for Name: hr_religion; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_religion (id, create_uid, create_date, name, write_uid, write_date, religion_code) VALUES (7, 1, '2016-09-12 10:56:57.727078', 'Catholic', 1, '2016-09-12 10:56:57.727078', '00001');
INSERT INTO hr_religion (id, create_uid, create_date, name, write_uid, write_date, religion_code) VALUES (8, 1, '2016-09-12 10:56:57.727078', 'Islam', 1, '2016-09-12 10:56:57.727078', '00002');
INSERT INTO hr_religion (id, create_uid, create_date, name, write_uid, write_date, religion_code) VALUES (9, 1, '2016-09-12 10:56:57.727078', 'Protestant', 1, '2016-09-12 10:56:57.727078', '00003');
INSERT INTO hr_religion (id, create_uid, create_date, name, write_uid, write_date, religion_code) VALUES (10, 1, '2016-09-12 10:56:57.727078', 'Born-Again Christian', 1, '2016-09-12 10:56:57.727078', '00004');
INSERT INTO hr_religion (id, create_uid, create_date, name, write_uid, write_date, religion_code) VALUES (11, 1, '2016-09-12 10:56:57.727078', 'Charismatic', 1, '2016-09-12 10:56:57.727078', '00005');
INSERT INTO hr_religion (id, create_uid, create_date, name, write_uid, write_date, religion_code) VALUES (12, 1, '2016-09-12 10:56:57.727078', 'INC', 1, '2016-09-12 10:56:57.727078', '00006');


--
-- Name: hr_religion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_religion_id_seq', 12, true);


--
-- PostgreSQL database dump complete
--

