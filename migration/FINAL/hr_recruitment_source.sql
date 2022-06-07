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
-- Data for Name: hr_recruitment_source; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_recruitment_source (id, create_uid, create_date, name, write_uid, write_date, source_id) VALUES (1, 1, '2016-09-12 10:33:32.720694', 'LinkedIn', 1, '2016-09-12 10:33:32.720694', 6);
INSERT INTO hr_recruitment_source (id, create_uid, create_date, name, write_uid, write_date, source_id) VALUES (2, 1, '2016-09-12 10:33:32.720694', 'Monster', 1, '2016-09-12 10:33:32.720694', 7);
INSERT INTO hr_recruitment_source (id, create_uid, create_date, name, write_uid, write_date, source_id) VALUES (3, 1, '2016-09-12 10:33:32.720694', 'Word of Mouth', 1, '2016-09-12 10:33:32.720694', 10);
INSERT INTO hr_recruitment_source (id, create_uid, create_date, name, write_uid, write_date, source_id) VALUES (4, 1, '2016-09-12 10:33:32.720694', 'Company Website', 1, '2016-09-12 10:33:32.720694', 11);


--
-- Name: hr_recruitment_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_recruitment_source_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

