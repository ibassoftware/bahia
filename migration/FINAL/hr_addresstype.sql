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
-- Data for Name: hr_addresstype; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (1, 1, '2016-09-12 10:39:27.500805', NULL, 1, '2016-09-12 10:39:27.500805', 'Permanent');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (2, 1, '2016-09-12 10:39:32.881492', NULL, 1, '2016-09-12 10:39:35.97118', 'Temporary');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (3, 1, '2016-09-23 03:54:22.429013', NULL, 1, '2016-09-23 03:54:22.429013', 'P-6A BALANGHAI');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (4, 30049, '2016-09-28 00:06:44.798425', NULL, 30049, '2016-09-28 00:06:44.798425', 'alternate');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (5, 30065, '2016-10-06 07:43:46.844883', NULL, 30065, '2016-10-06 07:43:46.844883', 'B29 L11');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (6, 30047, '2016-11-10 07:02:46.130829', NULL, 30047, '2016-11-10 07:02:46.130829', '94 BRGY ALACAN');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (7, 30047, '2016-11-10 07:35:25.314864', NULL, 30047, '2016-11-10 07:35:25.314864', 'SAYAO');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (8, 30050, '2016-11-16 06:56:40.859599', NULL, 30050, '2016-11-16 06:56:40.859599', 'STA LUCIA RESSTLEMENT MAGALANG ');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (9, 30057, '2016-12-13 23:28:03.464891', NULL, 30057, '2016-12-13 23:28:03.464891', '538 GRACIA ST. MARICK SUBD BRGY STO DOMINGO');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (10, 30047, '2017-01-10 02:40:48.704163', NULL, 30047, '2017-01-10 02:40:48.704163', '128 CORDILLERA STREET');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (11, 30047, '2017-01-21 02:32:30.940517', NULL, 30047, '2017-01-21 02:32:30.940517', 'GUTAD');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (12, 30047, '2017-01-21 03:13:49.980909', NULL, 30047, '2017-01-21 03:13:49.980909', 'CABATIANUHAN');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (13, 30047, '2017-01-21 03:40:19.575845', NULL, 30047, '2017-01-21 03:40:19.575845', '299 BRGY CABLONG ROAD 1');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (14, 30065, '2017-09-13 03:09:40.49611', NULL, 30065, '2017-09-13 03:09:40.49611', '1247 J. TAYABAS ST');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (15, 30065, '2018-01-23 00:56:11.796697', NULL, 30065, '2018-01-23 00:56:11.796697', 'Alternate');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (16, 30049, '2018-08-13 01:13:17.288728', NULL, 30049, '2018-08-13 01:13:17.288728', 'PER');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (17, 30075, '2018-10-10 03:00:57.782514', NULL, 30075, '2018-10-10 03:00:57.782514', 'B25 L41 P2 AREA 1');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (18, 30047, '2020-11-17 00:24:57.513462', NULL, 30047, '2020-11-17 00:24:57.513462', '#42 President Garcia St.');
INSERT INTO hr_addresstype (id, create_uid, create_date, description, write_uid, write_date, name) VALUES (19, 30047, '2020-11-19 23:42:30.683106', NULL, 30047, '2020-11-19 23:42:30.683106', 'SAN VICTOR');


--
-- Name: hr_addresstype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_addresstype_id_seq', 19, true);


--
-- PostgreSQL database dump complete
--

