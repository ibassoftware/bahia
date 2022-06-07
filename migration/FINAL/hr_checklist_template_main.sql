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
-- Data for Name: hr_checklist_template_main; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_checklist_template_main (id, create_uid, create_date, name, write_uid, allow_to_fill_by_dep, write_date) VALUES (1, 1, '2017-09-08 04:16:20.015648', 'Default Template', 1, false, '2019-10-14 01:13:33.041885');


--
-- Name: hr_checklist_template_main_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_checklist_template_main_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

