# -*- coding: utf-8 -*-

class TestPGConnection(object):
    queries = []

    async def execute(self, *args, **kwargs):
        self.queries.append(args)

    async def close(self, *args, **kwargs):
        pass


test_pg_connection = TestPGConnection()


class TestCrateCursor(object):
    queries = []

    def execute(self, *args, **kwargs):
        self.queries.append(args)

    def executemany(self, *args, **kwargs):
        self.queries.append(args)

    def close(self, *args, **kwargs):
        pass


test_crate_cursor = TestCrateCursor()


class TestCrateConnection(object):
    @staticmethod
    def cursor(*args, **kwargs):
        return test_crate_cursor

    @staticmethod
    def close(*args, **kwargs):
        pass
