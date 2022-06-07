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
-- Data for Name: hr_documenttype; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (16, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'Bahamas', '2016-09-18 04:17:33.91416', 'Bahamas Seamansbook', NULL);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (18, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'Marshall Is', '2016-09-18 04:17:33.91416', 'Marshall Islands Seamansbook', NULL);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (19, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'Liberia', '2016-09-18 04:17:33.91416', 'Liberian Seamansbook', NULL);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (20, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'Panama', '2016-09-18 04:17:33.91416', 'Panamanian Seamansbook', NULL);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (21, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'No', '2016-09-18 04:17:33.91416', 'Norwegian Booklet', NULL);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (22, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'MCV', '2016-09-18 04:17:33.91416', 'Maritime Crew Visa', NULL);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (24, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'YF', '2016-09-18 04:17:33.91416', 'Yellow Fever', NULL);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (13, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'P', '2016-09-27 07:11:04.656296', 'Phil Passport', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (14, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'V', '2016-09-27 07:11:09.332757', 'US VISA', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (15, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'SSRB', '2016-09-27 07:11:13.480286', 'Phil Seamansbook', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (23, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'UK', '2016-09-27 07:53:57.097385', 'UKTransit Visa', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (28, 30065, '2016-10-06 05:49:10.959006', NULL, 30065, 'SCHENGEN VISA', '2016-10-06 05:49:10.959006', 'SCHENGEN VISA', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (41, 1, '2017-10-24 00:24:17.504354', 'Overseas Employment Certificate', 1, 'OEC', '2017-10-24 00:24:17.504354', 'OEC', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (43, 30065, '2018-06-18 06:21:30.066561', NULL, 30065, 'Malta SBook', '2018-06-18 06:21:30.066561', 'Maltese SBook', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (46, 30078, '2018-08-28 06:02:02.411887', NULL, 30078, 'CYPRUS', '2018-08-28 06:02:02.411887', 'CYPRUS', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (50, 30078, '2018-09-11 05:22:44.139397', NULL, 30078, 'BasicTraining', '2018-09-11 05:22:44.139397', 'Basic Training', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (52, 30078, '2018-09-11 05:25:30.761366', NULL, 30078, 'Marine Engineering', '2018-09-11 05:25:30.761366', 'Marine Engineering', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (55, 30047, '2018-10-12 03:09:40.330114', NULL, 30047, 'AUS', '2018-10-12 03:09:40.330114', 'AUSTRALIAN VISA', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (57, 30047, '2018-10-29 07:24:42.169588', NULL, 30047, 'UK6', '2018-10-29 07:24:42.169588', 'UK6M', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (59, 30047, '2018-10-29 07:25:20.322021', NULL, 30047, 'UK6V', '2018-10-29 07:25:20.322021', 'UK6M C-VISIT', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (17, 1, '2016-09-18 04:17:33.91416', NULL, 1, 'SRC E-REG', '2018-11-13 01:41:06.102843', 'SRC E-REG', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (64, 30075, '2018-12-17 04:52:46.241754', NULL, 30075, 'MARITIME CREW VISA', '2018-12-17 04:52:46.241754', 'MCV', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (70, 30078, '2019-01-07 06:54:24.340888', NULL, 30078, 'ratings forming navigational watch ', '2019-01-07 06:54:24.340888', 'ratings forming navigational watch ', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (73, 30078, '2019-01-07 07:01:22.131101', NULL, 30078, 'SDSD', '2019-01-07 07:01:22.131101', 'SDSD', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (75, 30078, '2019-01-07 07:01:51.905894', NULL, 30078, 'PSCRB', '2019-01-07 07:01:51.905894', 'PSCRB', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (77, 30078, '2019-01-07 07:03:54.859331', NULL, 30078, 'BTOC', '2019-01-07 07:03:54.859331', 'BTOC', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (79, 30078, '2019-01-07 07:05:36.623932', NULL, 30078, 'ISM', '2019-01-07 07:05:36.623932', 'ISM', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (81, 30078, '2019-01-07 07:07:17.826739', NULL, 30078, 'maritime english', '2019-01-07 07:07:17.826739', 'Maritime english', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (87, 30049, '2019-05-23 06:37:54.021676', NULL, 30049, 'A', '2019-05-23 06:37:54.021676', 'SRN', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (89, 30065, '2019-06-17 05:16:40.942181', 'SRC', 30065, 'SRC', '2019-06-17 05:16:40.942181', 'SRC', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (93, 30047, '2019-10-04 02:13:51.841392', NULL, 30047, 'US', '2019-10-04 02:13:51.841392', 'US B1/B2', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (95, 1, '2020-01-24 01:15:26.3082', 'Membership', 1, 'OWWA', '2020-01-24 01:15:26.3082', 'OWWA', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (99, 30065, '2020-09-30 05:22:25.564948', NULL, 30065, 'Taiwanese', '2020-09-30 05:22:25.564948', 'Taiwanese ', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (100, 30078, '2021-07-01 08:47:09.257706', NULL, 30078, 'UK VISA', '2021-07-01 08:47:09.257706', 'UK VISA', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (103, 30048, '2021-08-18 03:09:39.329746', NULL, 30048, 'PDOS', '2021-08-18 03:09:39.329746', 'PDOS', true);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (104, 30048, '2021-08-18 03:27:46.926382', NULL, 30048, 'PDOS', '2021-08-18 03:27:46.926382', 'PDOS CARD', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (106, 30048, '2021-08-18 04:06:04.03521', NULL, 30048, 'PDOS', '2021-08-18 04:06:04.03521', 'PDOS CARD', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (112, 30065, '2021-10-15 02:27:32.318674', NULL, 30065, 'Taiwanese Visa', '2021-10-15 02:27:32.318674', 'Taiwanese Visa', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (114, 30047, '2021-10-18 08:36:22.429121', NULL, 30047, '200', '2021-10-18 08:36:22.429121', 'MISMO', false);
INSERT INTO hr_documenttype (id, create_uid, create_date, description, write_uid, abbreviation, write_date, name, check_for_expiration) VALUES (116, 30047, '2021-10-18 08:36:42.634039', NULL, 30047, '2001', '2021-10-18 08:36:42.634039', 'MISMO SRN', false);


--
-- Name: hr_documenttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_documenttype_id_seq', 118, true);


--
-- PostgreSQL database dump complete
--

