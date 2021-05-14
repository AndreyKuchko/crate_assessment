# -*- coding: utf-8; -*-
import asyncio

from crate_vbb_importer.models import ALL_MODELS
from crate_vbb_importer.utils.commands.base import BaseAsyncCommand


class Command(BaseAsyncCommand):
    """ Drops all related tables from database
    """

    async def process(self, model):
        conn = await self.create_connection()
        obj = model(conn)
        await obj.drop_async()
        await conn.close()

    async def async_run(self):
        await asyncio.gather(*[self.process(m) for m in ALL_MODELS])
