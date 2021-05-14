# -*- coding: utf-8; -*-
import asyncio
import logging
import os
from time import time

import asyncpg

from crate_vbb_importer.models import ALL_MODELS
from crate_vbb_importer.utils.logging import get_logger


class BaseCommand(object):
    def __init__(self, args, remaining_args, argparser, **_):
        self.args = args
        self.remaining_args = remaining_args
        self.logger = get_logger(args.log_level)
        self.validate_args(argparser)

    @staticmethod
    def prepare_argparser(parser):
        parser.add_argument(
            '--host',
            dest='host',
            type=str,
            default='localhost',
            help='CrateDB host'
        )
        parser.add_argument(
            '-u', '--user',
            dest='user',
            type=str,
            default='crate',
            help='CrateDB user'
        )
        parser.add_argument(
            '-p', '--password',
            dest='password',
            type=str,
            default=None,
            help='CrateDB password'
        )
        parser.add_argument(
            '-s', '--schema',
            dest='schema',
            type=str,
            default='doc',
            help='CrateDB schema'
        )
        parser.add_argument(
            '-d', '--data-dir',
            dest='data_dir',
            type=str,
            default='datasource',
            help='Directory with csv files'
        )
        parser.add_argument(
            '-b', '--batch-size',
            dest='batch_size',
            type=int,
            default=300,
            help='Insert batch size'
        )
        parser.add_argument(
            '-l', '--log-level',
            dest='log_level',
            type=str,
            choices=list(logging._nameToLevel.keys()),
            default='INFO',
            help='Log level'
        )

    def validate_args(self, argparser):
        data_dir = self.args.data_dir
        for model in ALL_MODELS:
            path = os.path.join(data_dir, model.source_file)
            if not os.path.exists(path):
                argparser.error(
                    'data directory doesn\'t contain necessary files. '
                    'Can\'t find {}'.format(path)
                )
        self.validate_connection(argparser)

    def run(self):
        start = time()
        result = self.do_run()
        self.logger.info(
            'Finished! It took {:.3f} seconds in total'.format(time() - start)
        )
        return result

    def do_run(self):
        raise NotImplementedError

    def validate_connection(self, argparser):
        raise NotImplementedError


class BaseAsyncCommand(BaseCommand):
    def __init__(self, args, remaining_args, argparser, **kwargs):
        self.loop = kwargs.pop('loop', asyncio.get_event_loop())
        super().__init__(args, remaining_args, argparser, **kwargs)

    @staticmethod
    def prepare_argparser(parser):
        BaseCommand.prepare_argparser(parser)
        parser.add_argument(
            '--port',
            dest='port',
            type=int,
            default=5432,
            help='CrateDB port'
        )

    async def create_connection(self):
        auth = self.args.user
        if self.args.password is not None:
            auth = '{}:{}'.format(auth, self.args.password)
        return await asyncpg.connect(
            'postgres://{}@{}:{}/{}'.format(
                auth, self.args.host, self.args.port, self.args.schema
            )
        )

    async def do_validate_connection(self):
        connection = await self.create_connection()
        await connection.execute('SELECT 1')
        await connection.close()

    def validate_connection(self, argparser):
        try:
            self.loop.run_until_complete(self.do_validate_connection())
        except Exception as e:
            self.logger.error(e)
            argparser.error(
                'Can\'t connect to database, please check connection parameters'
            )

    def do_run(self):
        try:
            return self.loop.run_until_complete(self.async_run())
        finally:
            self.loop.run_until_complete(self.async_on_complete())

    async def async_on_complete(self):
        pass

    async def async_run(self):
        raise NotImplementedError
