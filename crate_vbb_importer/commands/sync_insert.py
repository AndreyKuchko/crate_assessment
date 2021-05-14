# -*- coding: utf-8; -*-
import os
from csv import reader
from time import time

from crate import client

from crate_vbb_importer.models import ALL_MODELS
from crate_vbb_importer.utils.commands.base import BaseCommand


class Command(BaseCommand):
    """ Perform sync insert of data from csv files to CrateDB
    """

    @staticmethod
    def prepare_argparser(parser):
        BaseCommand.prepare_argparser(parser)
        parser.add_argument(
            '--port',
            dest='port',
            type=int,
            default=4200,
            help='CrateDB port'
        )
        parser.add_argument(
            '-t', '--timeout',
            dest='timeout',
            type=int,
            default=10,
            help='CrateDB connection timeout'
        )

    def create_connection(self):
        return client.connect(
            '{}:{}'.format(self.args.host, self.args.port),
            username=self.args.user,
            password=self.args.password,
            schema=self.args.schema,
            timeout=self.args.timeout
        )

    def validate_connection(self, argparser):
        try:
            connection = self.create_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            connection.close()
        except Exception as e:
            self.logger.error(e)
            argparser.error(
                'Can\'t connect to database, please check connection parameters'
            )

    def do_run(self):
        connection = self.create_connection()
        cursor = connection.cursor()
        for model in ALL_MODELS:
            start = time()
            obj = model(cursor, self.args.batch_size)
            obj.create_table()
            file_path = os.path.join(self.args.data_dir, obj.source_file)
            lines_counter = 0
            with open(file_path) as csv_file:
                csv_reader = reader(csv_file, delimiter=',')
                next(csv_reader)  # skip header
                for row in csv_reader:
                    obj.process_row(row)
                    lines_counter += 1
                obj.finalize()
            self.logger.info(
                'Processing of {} was finished. It took {:.3f} seconds, {} csv '
                'lines were processed.'.format(
                    obj.source_file, time() - start, lines_counter
                )
            )
        cursor.close()
        connection.close()
