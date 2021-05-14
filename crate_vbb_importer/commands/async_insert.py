# -*- coding: utf-8; -*-
import asyncio
import os
from csv import reader
from time import time

from crate_vbb_importer.models import ALL_MODELS
from crate_vbb_importer.utils.commands.base import BaseAsyncCommand


class Command(BaseAsyncCommand):
    """ Perform async insert of data from csv files to CrateDB
    """

    async def process(self, model):
        conn = await self.create_connection()
        obj = model(conn)
        await obj.drop_async()
        await conn.close()

        start = time()
        conn = await self.create_connection()
        obj = model(conn, self.args.batch_size)
        await obj.create_table_async()
        file_path = os.path.join(self.args.data_dir, obj.source_file)
        lines_counter = 0
        with open(file_path) as csv_file:
            csv_reader = reader(csv_file, delimiter=',')
            next(csv_reader)  # skip header
            for row in csv_reader:
                await obj.process_row_async(row)
                lines_counter += 1
            await obj.finalize_async()
        await conn.close()
        self.logger.info(
            'Processing of {} was finished. It took {:.3f} seconds, {} csv '
            'lines were processed.'.format(
                obj.source_file, time() - start, lines_counter
            )
        )

    async def async_run(self):
        await asyncio.gather(*[self.process(m) for m in ALL_MODELS])
