# -*- coding: utf-8 -*-
import os
import argparse

from crate_vbb_importer.commands.async_insert import Command as AsyncInsertCommand
from crate_vbb_importer.commands.clean import Command as CleanCommand
from crate_vbb_importer.commands.sync_insert import Command as SyncInsertCommand

from tests.utils import test_pg_connection, test_crate_cursor
from tests.expected_data import EXPECTED_ASYNC_INSERT, EXPECTED_CLEAN, EXPECTED_SYNC_INSERT


def test_clean():
    parser = argparse.ArgumentParser()
    CleanCommand.prepare_argparser(parser)
    raw_args = ('--host', 'test_host', '-d', os.path.join('tests', 'testdata'))
    args, remaining_args = parser.parse_known_args(raw_args)
    args.command_name = 'clean'
    command = CleanCommand(args, remaining_args, parser)
    command.run()
    assert test_pg_connection.queries == EXPECTED_CLEAN
    test_pg_connection.queries = []


def test_async_insert():
    parser = argparse.ArgumentParser()
    AsyncInsertCommand.prepare_argparser(parser)
    raw_args = ('--host', 'test_host', '-d', os.path.join('tests', 'testdata'), '-b', '2')
    args, remaining_args = parser.parse_known_args(raw_args)
    args.command_name = 'async_insert'
    command = AsyncInsertCommand(args, remaining_args, parser)
    command.run()
    assert test_pg_connection.queries == EXPECTED_ASYNC_INSERT
    test_pg_connection.queries = []


def test_sync_insert():
    parser = argparse.ArgumentParser()
    SyncInsertCommand.prepare_argparser(parser)
    raw_args = ('--host', 'test_host', '-d', os.path.join('tests', 'testdata'), '-b', '2')
    args, remaining_args = parser.parse_known_args(raw_args)
    args.command_name = 'sync_insert'
    command = SyncInsertCommand(args, remaining_args, parser)
    command.run()
    assert test_crate_cursor.queries == EXPECTED_SYNC_INSERT
    test_crate_cursor.queries = []
