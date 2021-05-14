# -*- coding: utf-8; -*-
import json
from datetime import date


class Converter(object):
    """ Set on functions for type-casting to prepare fields data to DB format
    """
    @staticmethod
    def get_plain_value(value):
        return value

    @staticmethod
    def get_int_value(value, default=None):
        if value == '':
            return default
        return int(value)

    @classmethod
    def get_int_value_with_default_0(cls, value):
        return cls.get_int_value(value, 0)

    @staticmethod
    def get_float_value(value):
        if value == '':
            return None
        return float(value)

    @staticmethod
    def get_time_value(value):
        (hours, minutes, seconds) = value.split(':')
        return int(seconds) + 60 * int(minutes) + 3600 * int(hours)

    @staticmethod
    def get_boolean_value(value):
        if value == '0':
            return False
        else:
            return True

    @staticmethod
    def get_date_value(value):
        return date(int(value[:4]), int(value[4:-2]), int(value[-2:]))

    @staticmethod
    def get_color_value(value, default='FFFFFF'):
        if value == '':
            value = default
        return int(value, 16)

    @classmethod
    def get_text_color_value(cls, value):
        return cls.get_color_value(value, '000000')

    @staticmethod
    def get_point_value(value):
        return [float(value[0]), float(value[1])]

    @staticmethod
    def get_shape_value(value):
        points = ''
        for (lat, lon, ) in value:
            points += '{} {}, '.format(lon, lat)
        return 'LINESTRING ({})'.format(points[:-2])

    @staticmethod
    def get_shape_value_for_asyncpg(value):
        coordinates = []
        for (lat, lon, ) in value:
            coordinates.append([float(lon), float(lat)])
        return json.dumps({'type': 'LineString', 'coordinates': coordinates})
