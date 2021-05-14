# -*- coding: utf-8; -*-
from crate_vbb_importer.utils.fields import Converter as C


class BaseModel(object):
    table = None
    source_file = None
    fields = ()

    def __init__(self, executor, batch_size=None):
        self.executor = executor
        self.batch_size = batch_size
        self.insert_queue = []
        field_names = self.fields.keys()
        self.insert_sql = "INSERT INTO {} ({}) VALUES ({})".format(
            self.table,
            ', '.join(field_names),
            ', '.join('?' * len(field_names))
        )
        self.insert_sql_async = "INSERT INTO {} ({}) VALUES".format(
            self.table,
            ', '.join(field_names)
        )

    def create_table(self):
        fields_string = ''
        for name, field_meta in self.fields.items():
            field_type = field_meta[0]
            fields_string += '{} {}, '.format(name, field_type)

        sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(
            self.table, fields_string[:-2]
        )
        self.executor.execute(sql)

    async def create_table_async(self):
        fields_string = ''
        for name, field_meta in self.fields.items():
            field_type = field_meta[0]
            fields_string += '{} {}, '.format(name, field_type)

        sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(
            self.table, fields_string[:-2]
        )
        await self.executor.execute(sql)

    def bulk_insert(self):
        if self.insert_queue:
            self.executor.executemany(self.insert_sql, self.insert_queue)
        self.insert_queue = []

    async def bulk_insert_async(self):
        if self.insert_queue:
            one_row_values = '({})'.format(', '.join('?' * len(self.fields)))
            sql = '{} {}'.format(
                self.insert_sql_async,
                ', '.join([one_row_values] * len(self.insert_queue))
            )
            flatten_params = [
                item for sublist in self.insert_queue for item in sublist
            ]
            await self.executor.execute(sql, *flatten_params)
        self.insert_queue = []

    def process_row(self, row):
        self.insert_queue.append(self.get_insert_values(row))
        if len(self.insert_queue) >= self.batch_size:
            self.bulk_insert()

    async def process_row_async(self, row):
        self.insert_queue.append(tuple(self.get_insert_values(row)))
        if len(self.insert_queue) >= self.batch_size:
            await self.bulk_insert_async()

    @classmethod
    def get_insert_values(cls, values):
        result = []
        fields_meta = list(cls.fields.values())
        for i, value in enumerate(values):
            result.append(fields_meta[i][1](value))

        return result

    def finalize(self):
        self.bulk_insert()

    async def finalize_async(self):
        await self.bulk_insert_async()

    async def drop_async(self):
        sql = "DROP TABLE IF EXISTS {}".format(self.table)
        await self.executor.execute(sql)


class Agency(BaseModel):
    table = 'agency'
    source_file = 'agency.txt'
    fields = {
        'agency_id': ('integer primary key', C.get_int_value, ),
        'agency_name': ('text', C.get_plain_value, ),
        'agency_url': ('text', C.get_plain_value, ),
        'agency_timezone': ('text', C.get_plain_value, ),
        'agency_lang': ('text', C.get_plain_value, ),
        'agency_phone': ('text', C.get_plain_value, ),
    }


class Calendar(BaseModel):
    table = 'calendar'
    source_file = 'calendar.txt'
    fields = {
        'service_id': ('integer primary key', C.get_int_value, ),
        'monday': ('boolean', C.get_boolean_value, ),
        'tuesday': ('boolean', C.get_boolean_value, ),
        'wednesday': ('boolean', C.get_boolean_value, ),
        'thursday': ('boolean', C.get_boolean_value, ),
        'friday': ('boolean', C.get_boolean_value, ),
        'saturday': ('boolean', C.get_boolean_value, ),
        'sunday': ('boolean', C.get_boolean_value, ),
        'start_date': ('timestamp without time zone', C.get_date_value, ),
        'end_date': ('timestamp without time zone', C.get_date_value, ),
    }


class CalendarDates(BaseModel):
    table = 'calendar_dates'
    source_file = 'calendar_dates.txt'
    fields = {
        'service_id': ('integer', C.get_int_value, ),
        'date': ('timestamp without time zone', C.get_date_value, ),
        'exception_type': ('smallint', C.get_int_value, ),
    }


class Frequencies(BaseModel):
    table = 'frequencies'
    source_file = 'frequencies.txt'
    fields = {
        'trip_id': ('integer primary key', C.get_int_value, ),
        'start_time': ('integer', C.get_time_value, ),
        'end_time': ('integer', C.get_time_value, ),
        'headway_secs': ('integer', C.get_int_value, ),
        'exact_times': ('boolean', C.get_boolean_value, ),
    }


class Pathways(BaseModel):
    table = 'pathways'
    source_file = 'pathways.txt'
    fields = {
        'pathway_id': ('integer primary key', C.get_int_value, ),
        'from_stop_id': ('text', C.get_plain_value, ),
        'to_stop_id': ('text', C.get_int_value, ),
        'pathway_mode': ('smallint', C.get_int_value, ),
        'is_bidirectional': ('boolean', C.get_boolean_value, ),
        'traversal_time': ('integer', C.get_int_value, ),
        'length': ('real', C.get_float_value, ),
        'stair_count': ('integer', C.get_int_value, ),
        'max_slope': ('real', C.get_float_value, ),
        'min_width': ('real', C.get_float_value, ),
    }


class Routes(BaseModel):
    table = 'routes'
    source_file = 'routes.txt'
    fields = {
        'route_id': ('text primary key', C.get_plain_value, ),
        'agency_id': ('integer', C.get_int_value, ),
        'route_short_name': ('text', C.get_plain_value, ),
        'route_long_name': ('text', C.get_plain_value, ),
        'route_type': ('smallint', C.get_int_value, ),
        'route_color': ('integer', C.get_color_value, ),
        'route_text_color': ('integer', C.get_text_color_value, ),
        'route_desc': ('text', C.get_plain_value, ),
    }


class Shapes(BaseModel):
    table = 'shapes'
    source_file = 'shapes.txt'
    fields = {
        'shape_id': ('integer primary key', C.get_int_value, ),
        'shape': ('geo_shape', C.get_shape_value, ),
    }

    def __init__(self, cursor, batch_size=None):
        self.shape_points = []
        self.current_shape_id = None
        super().__init__(cursor, batch_size)

    @classmethod
    def get_insert_values_for_asyncpg(cls, values):
        result = []
        fields_meta = list(cls.fields.values())
        for i, value in enumerate(values):
            if fields_meta[i][0] == 'geo_shape':
                res_value = C.get_shape_value_for_asyncpg(value)
            else:
                res_value = fields_meta[i][1](value)
            result.append(res_value)

        return result

    def _process_row(self, row, convert_func):
        shape_id = row[0]
        point = (row[1], row[2], )
        if self.current_shape_id is None:
            self.current_shape_id = shape_id

        if self.current_shape_id != shape_id:
            # save current shape and start collecting points for next shape
            row = (self.current_shape_id, self.shape_points, )
            self.insert_queue.append(convert_func(row))
            self.shape_points = [point]
            self.current_shape_id = shape_id
        else:
            # add point to current shape
            self.shape_points.append(point)

    def process_row(self, row):
        self._process_row(row, self.get_insert_values)
        if len(self.insert_queue) >= self.batch_size:
            self.bulk_insert()

    async def process_row_async(self, row):
        self._process_row(row, self.get_insert_values_for_asyncpg)
        if len(self.insert_queue) >= self.batch_size:
            await self.bulk_insert_async()

    def finalize(self):
        last_row = (self.current_shape_id, self.shape_points, )
        self.insert_queue.append(self.get_insert_values(last_row))
        self.bulk_insert()

    async def finalize_async(self):
        last_row = (self.current_shape_id, self.shape_points, )
        self.insert_queue.append(self.get_insert_values_for_asyncpg(last_row))
        await self.bulk_insert_async()


class StopTimes(BaseModel):
    table = 'stop_times'
    source_file = 'stop_times.txt'
    fields = {
        'trip_id': ('integer', C.get_int_value, ),
        'arrival_time': ('integer', C.get_time_value, ),
        'departure_time': ('integer', C.get_time_value, ),
        'stop_id': ('text', C.get_plain_value, ),
        'stop_sequence': ('integer', C.get_int_value, ),
        'pickup_type': ('smallint', C.get_int_value_with_default_0, ),
        'drop_off_type': ('smallint', C.get_int_value_with_default_0, ),
        'stop_headsign': ('text', C.get_plain_value, ),
    }


class Stops(BaseModel):
    table = 'stops'
    source_file = 'stops.txt'
    fields = {
        'stop_id': ('text primary key', C.get_plain_value, ),
        'stop_code': ('text', C.get_plain_value, ),
        'stop_name': ('text', C.get_plain_value, ),
        'stop_desc': ('text', C.get_plain_value, ),
        'location': ('geo_point', C.get_point_value, ),
        'location_type': ('smallint', C.get_int_value_with_default_0, ),
        'parent_station': ('text', C.get_plain_value, ),
        'wheelchair_boarding': ('smallint', C.get_int_value_with_default_0, ),
        'platform_code': ('text', C.get_plain_value, ),
        'zone_id': ('text', C.get_plain_value, ),
    }

    @classmethod
    def get_insert_values(cls, values):
        # replace separate lat and lan to tuple (lan, lat, )
        values[4] = (values[5], values[4], )
        del values[5]
        return super().get_insert_values(values)


class Transfers(BaseModel):
    table = 'transfers'
    source_file = 'transfers.txt'
    fields = {
        'from_stop_id': ('text', C.get_plain_value, ),
        'to_stop_id': ('text', C.get_plain_value, ),
        'transfer_type': ('smallint', C.get_int_value, ),
        'min_transfer_time': ('integer', C.get_int_value, ),
        'from_route_id': ('text', C.get_plain_value, ),
        'to_route_id': ('text', C.get_plain_value, ),
        'from_trip_id': ('integer', C.get_int_value, ),
        'to_trip_id': ('integer', C.get_int_value, ),
    }


class Trips(BaseModel):
    table = 'trips'
    source_file = 'trips.txt'
    fields = {
        'route_id': ('text', C.get_plain_value, ),
        'service_id': ('integer', C.get_int_value, ),
        'trip_id': ('integer primary key', C.get_int_value, ),
        'trip_headsign': ('text', C.get_plain_value, ),
        'trip_short_name': ('text', C.get_plain_value, ),
        'direction_id': ('smallint', C.get_int_value, ),
        'block_id': ('text', C.get_plain_value, ),
        'shape_id': ('integer', C.get_int_value, ),
        'wheelchair_accessible': ('smallint', C.get_int_value_with_default_0, ),
        'bikes_allowed': ('smallint', C.get_int_value_with_default_0, ),
    }


ALL_MODELS = (
    Agency,
    Calendar,
    CalendarDates,
    Frequencies,
    Pathways,
    Routes,
    Shapes,
    StopTimes,
    Stops,
    Transfers,
    Trips,
)
