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
-- Data for Name: hr_ship_department; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (89, 1, '2016-09-12 10:53:28.603366', '[33000] Hotel', 1, '2016-09-12 10:53:28.603366', 'Hotel', '33000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (90, 1, '2016-09-12 10:53:28.603366', '[44000] Bar', 1, '2016-09-12 10:53:28.603366', 'Bar', '44000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (92, 1, '2016-09-12 10:53:28.603366', '[66000] Galley', 1, '2016-09-12 10:53:28.603366', 'Galley', '66000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (94, 1, '2016-09-12 10:53:28.603366', '[88000] Entertainment', 1, '2016-09-12 10:53:28.603366', 'Entertainment', '88000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (95, 1, '2016-09-12 10:53:28.603366', '[88500] Excursions', 1, '2016-09-12 10:53:28.603366', 'Excursions', '88500');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (96, 1, '2016-09-12 10:53:28.603366', '[90000] Gift Shop', 1, '2016-09-12 10:53:28.603366', 'Gift Shop', '90000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (97, 1, '2016-09-12 10:53:28.603366', '[90200] Beauty Shop', 1, '2016-09-12 10:53:28.603366', 'Beauty Shop', '90200');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (98, 1, '2016-09-12 10:53:28.603366', '[90300] Photoshop', 1, '2016-09-12 10:53:28.603366', 'Photoshop', '90300');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (99, 1, '2016-09-12 10:53:28.603366', '[90400] Casino', 1, '2016-09-12 10:53:28.603366', 'Casino', '90400');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (100, 1, '2016-09-12 10:53:28.603366', '[XXX] XXX', 1, '2016-09-12 10:53:28.603366', 'XXX', 'XXX');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (101, 1, '2016-09-12 10:53:28.603366', '[C] Catering', 1, '2016-09-12 10:53:28.603366', 'Catering', 'C');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (102, 1, '2016-09-12 10:53:28.603366', '[10000] Deck- Non-pax', 1, '2016-09-12 10:53:28.603366', 'Deck- Non-pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (103, 1, '2016-09-12 10:53:28.603366', '[20000] Engine - Non-pax', 1, '2016-09-12 10:53:28.603366', 'Engine - Non-pax', '20000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (104, 1, '2016-09-12 10:53:28.603366', '[30000] Catering - Non-pax', 1, '2016-09-12 10:53:28.603366', 'Catering - Non-pax', '30000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (105, 1, '2016-09-12 10:53:28.603366', '[A1100] Deck', 1, '2016-09-12 10:53:28.603366', 'Deck', 'A1100');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (106, 1, '2016-09-12 10:53:28.603366', '[A2200] Engine', 1, '2016-09-12 10:53:28.603366', 'Engine', 'A2200');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (107, 1, '2016-09-12 10:53:28.603366', '[A3300] Hotel', 1, '2016-09-12 10:53:28.603366', 'Hotel', 'A3300');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (108, 1, '2016-09-12 10:53:28.603366', '[A4400] Bar', 1, '2016-09-12 10:53:28.603366', 'Bar', 'A4400');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (109, 1, '2016-09-12 10:53:28.603366', '[A5500] Restaurant', 1, '2016-09-12 10:53:28.603366', 'Restaurant', 'A5500');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (110, 1, '2016-09-12 10:53:28.603366', '[A6600] Galley', 1, '2016-09-12 10:53:28.603366', 'Galley', 'A6600');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (111, 1, '2016-09-12 10:53:28.603366', '[A7700] Housekeeping', 1, '2016-09-12 10:53:28.603366', 'Housekeeping', 'A7700');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (112, 1, '2016-09-12 10:53:28.603366', '[A8800] Entertainment', 1, '2016-09-12 10:53:28.603366', 'Entertainment', 'A8800');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (113, 1, '2016-09-12 10:53:28.603366', '[A9900] Excursions', 1, '2016-09-12 10:53:28.603366', 'Excursions', 'A9900');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (114, 1, '2016-09-12 10:53:28.603366', '[B1100] Deck', 1, '2016-09-12 10:53:28.603366', 'Deck', 'B1100');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (115, 1, '2016-09-12 10:53:28.603366', '[B2200] Engine ', 1, '2016-09-12 10:53:28.603366', 'Engine ', 'B2200');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (116, 1, '2016-09-12 10:53:28.603366', '[B3300] Hotel', 1, '2016-09-12 10:53:28.603366', 'Hotel', 'B3300');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (117, 1, '2016-09-12 10:53:28.603366', '[B4400] Bar ', 1, '2016-09-12 10:53:28.603366', 'Bar ', 'B4400');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (118, 1, '2016-09-12 10:53:28.603366', '[B5500] Restaurant ', 1, '2016-09-12 10:53:28.603366', 'Restaurant ', 'B5500');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (119, 1, '2016-09-12 10:53:28.603366', '[B6600] Galley', 1, '2016-09-12 10:53:28.603366', 'Galley', 'B6600');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (120, 1, '2016-09-12 10:53:28.603366', '[B7700] Housekeeping ', 1, '2016-09-12 10:53:28.603366', 'Housekeeping ', 'B7700');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (121, 1, '2016-09-12 10:53:28.603366', '[B8800] Entertainment ', 1, '2016-09-12 10:53:28.603366', 'Entertainment ', 'B8800');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (122, 1, '2016-09-12 10:53:28.603366', '[B9900] Excursion ', 1, '2016-09-12 10:53:28.603366', 'Excursion ', 'B9900');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (123, 1, '2016-09-12 10:53:28.603366', '[90500] Spa Department', 1, '2016-09-12 10:53:28.603366', 'Spa Department', '90500');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (124, 1, '2016-09-26 12:52:41.40695', '[D] Deck', 1, '2016-09-26 12:52:41.40695', 'Deck', 'D');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (125, 1, '2016-10-03 06:06:45.502375', '[CRUISE] Cruise', 1, '2016-10-03 06:06:45.502375', 'Cruise', 'CRUISE');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (126, 1, '2016-10-03 06:14:04.27992', '[E] Engine', 1, '2016-10-03 06:14:04.27992', 'Engine', 'E');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (127, 1, '2016-10-03 06:39:31.079772', '[DECK] Deck', 1, '2016-10-03 06:39:31.079772', 'Deck', 'DECK');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (128, 1, '2016-10-04 00:07:57.15417', '[Housekeeping] Housekeeping', 1, '2016-10-04 00:07:57.15417', 'Housekeeping', 'Housekeeping');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (93, 1, '2016-09-12 10:53:28.603366', '[77000] Housekeeping', 1, '2016-10-04 00:11:45.579823', 'Housekeeping', '77000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (88, 1, '2016-09-12 10:53:28.603366', '[22000] Engine', 1, '2016-10-04 00:12:07.002579', 'Engine', '22000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (131, 30065, '2016-10-17 01:03:42.561353', '[Catering Non Pax] Room Stewardess', 30065, '2016-10-17 01:04:13.35646', 'Room Stewardess', 'Catering Non Pax');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (132, 30065, '2016-10-17 01:05:10.390325', '[Catering Non Pax] Room stewardess', 30065, '2016-10-17 01:05:10.390325', 'Room stewardess', 'Catering Non Pax');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (129, 30065, '2016-10-12 00:35:09.246335', '[Catering Non Pax] Room Stewardess', 30065, '2016-10-17 01:06:36.265556', 'Room Stewardess', 'Catering Non Pax');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (134, 30065, '2016-11-23 02:26:32.057958', '[[3000] - Catering Non Pax] Catering Non Pax', 30065, '2016-11-23 02:26:32.057958', 'Catering Non Pax', '[3000] - Catering Non Pax');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (87, 1, '2016-09-12 10:53:28.603366', '[10000] Deck - Non Pax', 30065, '2016-11-23 05:21:57.137458', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (136, 30065, '2016-11-23 05:29:14.036804', '[20000] Engine - Non Pax', 30065, '2016-11-23 05:29:26.072667', 'Engine - Non Pax', '20000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (135, 30065, '2016-11-23 02:28:09.9238', '[30000] Catering - Non Pax', 30065, '2016-11-23 05:43:04.090218', 'Catering - Non Pax', '30000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (133, 30065, '2016-10-17 01:07:27.395272', '[30000] Catering - Non Pax', 30065, '2016-11-23 06:00:28.066827', 'Catering - Non Pax', '30000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (137, 30065, '2016-11-23 06:01:17.228922', '[30000] Catering - Non Pax', 30065, '2016-11-23 06:01:17.228922', 'Catering - Non Pax', '30000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (138, 30065, '2017-01-13 01:17:20.389563', '[ENGINE DEPT] ENGINE DEPT', 30065, '2017-01-13 01:17:20.389563', 'ENGINE DEPT', 'ENGINE DEPT');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (139, 30065, '2017-01-13 01:18:31.867572', '[OFFSHORE TANKER] ENGINE DEPT', 30065, '2017-01-13 01:18:31.867572', 'ENGINE DEPT', 'OFFSHORE TANKER');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (140, 30065, '2018-06-01 03:05:47.468478', '[Motorman] Motorman', 30065, '2018-06-01 03:06:11.941549', 'Motorman', 'Motorman');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (141, 30067, '2018-08-17 02:30:18.050287', '[[B2200] Engine ] Engine Department', 30067, '2018-08-17 02:30:18.050287', 'Engine Department', '[B2200] Engine ');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (142, 30067, '2018-08-17 02:30:50.977475', '[[B2200] Engine ] Engine', 30067, '2018-08-17 02:30:50.977475', 'Engine', '[B2200] Engine ');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (91, 1, '2016-09-12 10:53:28.603366', '[55000] Restaurant', 1, '2018-09-25 03:51:58.23708', 'Restaurant', '55000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (143, 30047, '2019-03-14 01:03:27.841096', '[Room Stewardess] Room Stewardess', 30047, '2019-03-14 01:03:51.671534', 'Room Stewardess', 'Room Stewardess');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (144, 30047, '2019-03-14 01:11:23.281905', '[30000] Catering - Non Pax', 30047, '2019-03-14 01:14:15.211357', 'Catering - Non Pax', '30000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (145, 30047, '2019-03-14 01:21:34.195969', '[30000] Catering - Non Pax', 30047, '2019-03-14 01:21:34.195969', 'Catering - Non Pax', '30000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (146, 30047, '2019-03-14 01:38:09.704446', '[10000] Deck - Non Pax', 30047, '2019-03-14 01:38:09.704446', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (148, 30065, '2019-05-15 08:00:45.393187', '[20000] Engine - Non Pax', 30065, '2019-05-15 08:00:45.393187', 'Engine - Non Pax', '20000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (147, 30065, '2019-05-15 07:53:21.59597', '[10000] Deck - Non Pax', 30065, '2019-05-20 06:35:10.950911', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (150, 30065, '2019-05-22 06:04:39.082791', '[10000] Deck - Non Pax', 30065, '2019-05-22 06:04:39.082791', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (151, 30065, '2019-05-23 07:25:36.346078', '[10000] Deck - Non Pax', 30065, '2019-05-23 07:25:36.346078', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (154, 1, '2019-07-08 07:25:44.955086', '[DNV] DIVING SUPPORT', 1, '2019-07-08 07:25:44.955086', 'DIVING SUPPORT', 'DNV');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (155, 1, '2019-07-08 07:34:07.866686', '[PSV] PSV', 1, '2019-07-08 07:34:07.866686', 'PSV', 'PSV');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (157, 30065, '2019-07-26 02:34:43.566584', '[10000] Deck - Non Pax', 30065, '2019-07-26 02:34:43.566584', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (153, 30065, '2019-06-26 22:58:24.451303', '[10000] Deck - Non Pax', 30065, '2019-07-26 02:37:16.964071', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (152, 30065, '2019-06-06 01:54:15.921234', '[10000] Deck - Non Pax', 30065, '2019-07-26 02:51:39.743771', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (149, 30065, '2019-05-20 06:30:54.10709', '[10000] Deck - Non Pax', 30065, '2019-07-26 02:53:40.059781', 'Deck - Non Pax', '10000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (158, 1, '2019-09-04 01:04:01.616831', '[Galley] Galley', 1, '2019-09-04 01:04:01.616831', 'Galley', 'Galley');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (159, 30065, '2019-10-08 04:22:57.871817', '[Cook] Cook', 30065, '2019-10-08 04:23:52.332549', 'Cook', 'Cook');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (160, 30065, '2019-10-08 04:31:28.600079', '[Ftr] Ftr', 30065, '2019-10-08 04:32:10.341369', 'Ftr', 'Ftr');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (161, 30065, '2020-01-22 01:41:25.52925', '[OS] OS', 30065, '2020-01-22 01:41:37.782862', 'OS', 'OS');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (162, 30065, '2020-02-04 03:45:05.206796', '[3/E] 3/E', 30065, '2020-02-04 03:45:05.206796', '3/E', '3/E');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (163, 30065, '2020-02-04 03:46:43.793732', '[3/E] Engine', 30065, '2020-02-04 03:46:43.793732', 'Engine', '3/E');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (164, 30065, '2020-12-18 02:07:16.278859', '[30000] Catering Non-pax', 30065, '2020-12-18 02:08:45.075822', 'Catering Non-pax', '30000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (130, 30065, '2016-10-17 00:56:38.154566', '[3000] Catering - Non Pax', 30065, '2020-12-18 02:09:05.354219', 'Catering - Non Pax', '3000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (165, 30065, '2021-03-17 02:35:06.986237', '[20000] Engine', 30065, '2021-03-17 02:35:18.946519', 'Engine', '20000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (166, 30065, '2021-03-17 02:37:10.469533', '[20000] Engine', 30065, '2021-03-17 02:37:10.469533', 'Engine', '20000');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (167, 30047, '2021-08-02 09:32:58.803123', '[MED] DECK', 30047, '2021-08-02 09:32:58.803123', 'DECK', 'MED');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (168, 30047, '2021-08-02 09:33:53.497325', '[MEDICAL ADMINISTRATOR] MEDICAL ADMINISTRATOR', 30047, '2021-08-02 09:33:53.497325', 'MEDICAL ADMINISTRATOR', 'MEDICAL ADMINISTRATOR');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (169, 30047, '2021-08-02 09:34:57.713302', '[MED] MEDICAL ADMINISTRATOR', 30047, '2021-08-02 09:34:57.713302', 'MEDICAL ADMINISTRATOR', 'MED');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (170, 30047, '2021-08-03 02:22:07.248592', '[2021] IVENTORY', 30047, '2021-08-03 02:22:07.248592', 'IVENTORY', '2021');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (171, 30047, '2021-08-03 02:22:43.090855', '[2021] INVENTORY', 30047, '2021-08-03 02:22:43.090855', 'INVENTORY', '2021');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (172, 30047, '2021-08-09 07:30:40.321593', '[2021] MEDICAL', 30047, '2021-08-09 07:30:40.321593', 'MEDICAL', '2021');
INSERT INTO hr_ship_department (id, create_uid, create_date, name, write_uid, write_date, department, ship_dept_code) VALUES (173, 30047, '2022-05-06 01:55:12.067591', '[2ND ETO] ENGINE', 30047, '2022-05-06 01:55:12.067591', 'ENGINE', '2ND ETO');


--
-- Name: hr_ship_department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hr_ship_department_id_seq', 173, true);


--
-- PostgreSQL database dump complete
--

