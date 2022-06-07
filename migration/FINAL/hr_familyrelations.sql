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
-- Data for Name: hr_familyrelations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (15, 1, 'C', '2016-09-12 10:39:03.531947', 'Child', 1, '2016-09-12 10:39:03.531947', 'Child');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (16, 1, 'O', '2016-09-12 10:39:03.531947', 'Other', 1, '2016-09-12 10:39:03.531947', 'Other');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (17, 1, 'S', '2016-09-12 10:39:03.531947', 'Spouse', 1, '2016-09-12 10:39:03.531947', 'Spouse');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (18, 1, 'L', '2016-09-12 10:39:03.531947', 'Live-in-partner', 1, '2016-09-12 10:39:03.531947', 'Live-in-partner');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (19, 1, 'P', '2016-09-12 10:39:03.531947', 'Parent', 1, '2016-09-12 10:39:03.531947', 'Parent');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (20, 1, 'F', '2016-09-12 10:39:03.531947', 'Father', 1, '2016-09-12 10:39:03.531947', 'Father');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (21, 1, 'M', '2016-09-12 10:39:03.531947', 'Mother', 1, '2016-09-12 10:39:03.531947', 'Mother');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (22, 1, 'SIS', '2016-09-12 10:39:03.531947', 'Sister', 1, '2016-09-12 10:39:03.531947', 'Sister');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (23, 1, 'BRO', '2016-09-12 10:39:03.531947', 'Brother', 1, '2016-09-12 10:39:03.531947', 'Brother');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (24, 1, 'FIANCEE', '2016-09-12 10:39:03.531947', 'Fiancee', 1, '2016-09-12 10:39:03.531947', 'Fiancee');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (25, 1, 'MA-IN LAW', '2016-09-12 10:39:03.531947', 'Mother in-law', 1, '2016-09-12 10:39:03.531947', 'Mother in-law');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (26, 1, 'GRANDMA', '2016-09-12 10:39:03.531947', 'Grandmother', 1, '2016-09-12 10:39:03.531947', 'Grandmother');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (27, 1, 'COUSIN', '2016-09-12 10:39:03.531947', 'Cousin', 1, '2016-09-12 10:39:03.531947', 'Cousin');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (28, 1, 'A', '2016-09-12 10:39:03.531947', 'Aunt', 1, '2016-09-12 10:39:03.531947', 'Aunt');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (31, 30065, '1', '2016-10-06 05:30:21.369728', 'WIFE', 30065, '2016-10-06 05:30:21.369728', 'WIFE');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (33, 30049, 'GRANDFATHER', '2016-11-02 06:40:58.412823', NULL, 30049, '2016-11-02 06:40:58.412823', 'GRANDFATHER');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (37, 30047, 'SON', '2017-01-21 02:41:38.553174', NULL, 30047, '2017-01-21 02:41:38.553174', 'SON');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (47, 30049, '1', '2018-06-04 06:11:13.561867', NULL, 30049, '2018-06-04 06:11:13.561867', 'Uncle');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (51, 30078, 'Brother in Law', '2018-09-11 06:04:01.262069', NULL, 30078, '2018-09-11 06:04:01.262069', 'Brother in law');
INSERT INTO hr_familyrelations (id, create_uid, code, create_date, description, write_uid, write_date, name) VALUES (53, 30078, 'Daughter', '2018-09-11 06:25:22.559035', NULL, 30078, '2018-09-11 06:25:22.559035', 'Daughter');


--
-- Name: hr_familyrelations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_familyrelations_id_seq', 56, true);


--
-- PostgreSQL database dump complete
--

