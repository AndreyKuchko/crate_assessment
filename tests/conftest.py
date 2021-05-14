# -*- coding: utf-8; -*-
import pytest

from tests.utils import test_pg_connection, TestCrateConnection


@pytest.fixture(scope='function', autouse=True)
def mock_asyncpg(monkeypatch):
    class asyncpg(object):
        @staticmethod
        async def connect(*args, **kwargs):
            assert args == ('postgres://crate@test_host:5432/doc',)
            assert kwargs == {}
            return test_pg_connection

    monkeypatch.setattr('crate_vbb_importer.utils.commands.base.asyncpg', asyncpg)


@pytest.fixture(scope='function', autouse=True)
def mock_crate(monkeypatch):
    class client(object):
        @staticmethod
        def connect(*args, **kwargs):
            assert args == ('test_host:4200',)
            assert kwargs == {'password': None, 'schema': 'doc', 'timeout': 10, 'username': 'crate'}
            return TestCrateConnection

    monkeypatch.setattr('crate_vbb_importer.commands.sync_insert.client', client)
