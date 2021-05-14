# -*- coding: utf-8 -*-
# flake8: noqa: E501
import datetime


EXPECTED_CLEAN = [
    ('SELECT 1', ),
    ('DROP TABLE IF EXISTS agency',),
    ('DROP TABLE IF EXISTS calendar',),
    ('DROP TABLE IF EXISTS calendar_dates',),
    ('DROP TABLE IF EXISTS frequencies',),
    ('DROP TABLE IF EXISTS pathways',),
    ('DROP TABLE IF EXISTS routes',),
    ('DROP TABLE IF EXISTS shapes',),
    ('DROP TABLE IF EXISTS stop_times',),
    ('DROP TABLE IF EXISTS stops',),
    ('DROP TABLE IF EXISTS transfers',),
    ('DROP TABLE IF EXISTS trips',)
]

EXPECTED_ASYNC_INSERT = [
    ('SELECT 1',),
    ('CREATE TABLE IF NOT EXISTS agency (agency_id integer primary key, agency_name text, agency_url text, agency_timezone text, agency_lang text, agency_phone text)',),
    ('INSERT INTO agency (agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone) VALUES (?, ?, ?, ?, ?, ?)', 841, 'mobus Märkisch-Oderland Bus GmbH', 'http://www.mo-bus.de', 'Europe/Berlin', 'de', '+493341-4494900'),
    ('CREATE TABLE IF NOT EXISTS calendar (service_id integer primary key, monday boolean, tuesday boolean, wednesday boolean, thursday boolean, friday boolean, saturday boolean, sunday boolean, start_date timestamp without time zone, end_date timestamp without time zone)',),
    ('INSERT INTO calendar (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 1, True, True, True, True, True, False, False, datetime.date(2021, 5, 12), datetime.date(2021, 12, 11)),
    ('CREATE TABLE IF NOT EXISTS calendar_dates (service_id integer, date timestamp without time zone, exception_type smallint)',),
    ('INSERT INTO calendar_dates (service_id, date, exception_type) VALUES (?, ?, ?)', 1, datetime.date(2021, 5, 24), 2),
    ('CREATE TABLE IF NOT EXISTS frequencies (trip_id integer primary key, start_time integer, end_time integer, headway_secs integer, exact_times boolean)',),
    ('CREATE TABLE IF NOT EXISTS pathways (pathway_id integer primary key, from_stop_id text, to_stop_id text, pathway_mode smallint, is_bidirectional boolean, traversal_time integer, length real, stair_count integer, max_slope real, min_width real)',),
    ('CREATE TABLE IF NOT EXISTS routes (route_id text primary key, agency_id integer, route_short_name text, route_long_name text, route_type smallint, route_color integer, route_text_color integer, route_desc text)',),
    ('INSERT INTO routes (route_id, agency_id, route_short_name, route_long_name, route_type, route_color, route_text_color, route_desc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', '19058_100', 108, 'RE3', '', 100, 16734464, 16777215, 'Wittenberg/Falkenberg <> Berlin <> Stralsund/Schwedt'),
    ('CREATE TABLE IF NOT EXISTS shapes (shape_id integer primary key, shape geo_shape)',),
    ('INSERT INTO shapes (shape_id, shape) VALUES (?, ?), (?, ?)', 210, '{"type": "LineString", "coordinates": [[13.066689, 52.390812], [13.067064, 52.390761], [13.066852, 52.390835]]}', 197, '{"type": "LineString", "coordinates": [[13.055803, 52.412714], [13.055535, 52.412692], [13.055298, 52.412684]]}'),
    ('CREATE TABLE IF NOT EXISTS stop_times (trip_id integer, arrival_time integer, departure_time integer, stop_id text, stop_sequence integer, pickup_type smallint, drop_off_type smallint, stop_headsign text)',),
    ('INSERT INTO stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type, stop_headsign) VALUES (?, ?, ?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?, ?, ?)', 148928020, 18300, 18300, '100000710003', 0, 0, 0, '', 148928020, 18420, 18420, '100000718801', 1, 0, 0, ''),
    ('INSERT INTO stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type, stop_headsign) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 148928020, 18510, 18510, '100000710503', 2, 0, 0, ''),
    ('CREATE TABLE IF NOT EXISTS stops (stop_id text primary key, stop_code text, stop_name text, stop_desc text, location geo_point, location_type smallint, parent_station text, wheelchair_boarding smallint, platform_code text, zone_id text)',),
    ('INSERT INTO stops (stop_id, stop_code, stop_name, stop_desc, location, location_type, parent_station, wheelchair_boarding, platform_code, zone_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', '900000006102', '', 'Berlin, Prinzenallee/Soldiner Str.', '', [13.386241, 52.558656], 1, '', 1, '', '900000006102 5656 Berlin, Prinzenallee/Soldiner Str.'),
    ('CREATE TABLE IF NOT EXISTS transfers (from_stop_id text, to_stop_id text, transfer_type smallint, min_transfer_time integer, from_route_id text, to_route_id text, from_trip_id integer, to_trip_id integer)',),
    ('INSERT INTO transfers (from_stop_id, to_stop_id, transfer_type, min_transfer_time, from_route_id, to_route_id, from_trip_id, to_trip_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', '000008010327', '000008010327', 2, 240, '', '', 157862046, 157882971),
    ('CREATE TABLE IF NOT EXISTS trips (route_id text, service_id integer, trip_id integer primary key, trip_headsign text, trip_short_name text, direction_id smallint, block_id text, shape_id integer, wheelchair_accessible smallint, bikes_allowed smallint)',),
    ('INSERT INTO trips (route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, block_id, shape_id, wheelchair_accessible, bikes_allowed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', '16734_700', 19, 158022204, 'Nennhausen, Schule', '', 0, '10372', 570, 1, 0)
]

EXPECTED_SYNC_INSERT = [
    ('SELECT 1',),
    ('CREATE TABLE IF NOT EXISTS agency (agency_id integer primary key, agency_name text, agency_url text, agency_timezone text, agency_lang text, agency_phone text)',),
    ('INSERT INTO agency (agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone) VALUES (?, ?, ?, ?, ?, ?)', [[841, 'mobus Märkisch-Oderland Bus GmbH', 'http://www.mo-bus.de', 'Europe/Berlin', 'de', '+493341-4494900']]),
    ('CREATE TABLE IF NOT EXISTS calendar (service_id integer primary key, monday boolean, tuesday boolean, wednesday boolean, thursday boolean, friday boolean, saturday boolean, sunday boolean, start_date timestamp without time zone, end_date timestamp without time zone)',),
    ('INSERT INTO calendar (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [[1, True, True, True, True, True, False, False, datetime.date(2021, 5, 12), datetime.date(2021, 12, 11)]]),
    ('CREATE TABLE IF NOT EXISTS calendar_dates (service_id integer, date timestamp without time zone, exception_type smallint)',),
    ('INSERT INTO calendar_dates (service_id, date, exception_type) VALUES (?, ?, ?)', [[1, datetime.date(2021, 5, 24), 2]]),
    ('CREATE TABLE IF NOT EXISTS frequencies (trip_id integer primary key, start_time integer, end_time integer, headway_secs integer, exact_times boolean)',),
    ('CREATE TABLE IF NOT EXISTS pathways (pathway_id integer primary key, from_stop_id text, to_stop_id text, pathway_mode smallint, is_bidirectional boolean, traversal_time integer, length real, stair_count integer, max_slope real, min_width real)',),
    ('CREATE TABLE IF NOT EXISTS routes (route_id text primary key, agency_id integer, route_short_name text, route_long_name text, route_type smallint, route_color integer, route_text_color integer, route_desc text)',),
    ('INSERT INTO routes (route_id, agency_id, route_short_name, route_long_name, route_type, route_color, route_text_color, route_desc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [['19058_100', 108, 'RE3', '', 100, 16734464, 16777215, 'Wittenberg/Falkenberg <> Berlin <> Stralsund/Schwedt']]),
    ('CREATE TABLE IF NOT EXISTS shapes (shape_id integer primary key, shape geo_shape)',),
    ('INSERT INTO shapes (shape_id, shape) VALUES (?, ?)', [[210, 'LINESTRING (13.066689 52.390812, 13.067064 52.390761, 13.066852 52.390835)'], [197, 'LINESTRING (13.055803 52.412714, 13.055535 52.412692, 13.055298 52.412684)']]),
    ('CREATE TABLE IF NOT EXISTS stop_times (trip_id integer, arrival_time integer, departure_time integer, stop_id text, stop_sequence integer, pickup_type smallint, drop_off_type smallint, stop_headsign text)',),
    ('INSERT INTO stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type, stop_headsign) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [[148928020, 18300, 18300, '100000710003', 0, 0, 0, ''], [148928020, 18420, 18420, '100000718801', 1, 0, 0, '']]),
    ('INSERT INTO stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type, stop_headsign) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [[148928020, 18510, 18510, '100000710503', 2, 0, 0, '']]),
    ('CREATE TABLE IF NOT EXISTS stops (stop_id text primary key, stop_code text, stop_name text, stop_desc text, location geo_point, location_type smallint, parent_station text, wheelchair_boarding smallint, platform_code text, zone_id text)',),
    ('INSERT INTO stops (stop_id, stop_code, stop_name, stop_desc, location, location_type, parent_station, wheelchair_boarding, platform_code, zone_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [['900000006102', '', 'Berlin, Prinzenallee/Soldiner Str.', '', [13.386241, 52.558656], 1, '', 1, '', '900000006102 5656 Berlin, Prinzenallee/Soldiner Str.']]),
    ('CREATE TABLE IF NOT EXISTS transfers (from_stop_id text, to_stop_id text, transfer_type smallint, min_transfer_time integer, from_route_id text, to_route_id text, from_trip_id integer, to_trip_id integer)',),
    ('INSERT INTO transfers (from_stop_id, to_stop_id, transfer_type, min_transfer_time, from_route_id, to_route_id, from_trip_id, to_trip_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [['000008010327', '000008010327', 2, 240, '', '', 157862046, 157882971]]),
    ('CREATE TABLE IF NOT EXISTS trips (route_id text, service_id integer, trip_id integer primary key, trip_headsign text, trip_short_name text, direction_id smallint, block_id text, shape_id integer, wheelchair_accessible smallint, bikes_allowed smallint)',),
    ('INSERT INTO trips (route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, block_id, shape_id, wheelchair_accessible, bikes_allowed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [['16734_700', 19, 158022204, 'Nennhausen, Schule', '', 0, '10372', 570, 1, 0]])
]
