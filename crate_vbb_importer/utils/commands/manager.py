# -*- coding: utf-8; -*-
import argparse
import inspect
import sys

from crate_vbb_importer.exceptions import CommandNotFound
from crate_vbb_importer.utils.commands.base import BaseCommand


class CommandManager:
    """ Wrapper around commands that makes available choosing of commands from
    common parent command(crate_vbb_importer)
    """
    def __init__(self, registry, raw_args=None):
        self.registry = registry
        self.argparser = argparse.ArgumentParser()
        self.subparsers = self.argparser.add_subparsers(
            dest='command_name',
            description='Command name to run',
            title='command_name',
        )
        self.subparsers.required = True

        self.raw_args = raw_args or sys.argv[1:]
        self.args = None
        self.remaining_args = None

    @property
    def command_name(self):
        return self.args.command_name

    def init_argparser(self):
        for attribute_name in filter(lambda attr: not attr.startswith('_'), dir(self.registry)):
            attribute = getattr(self.registry, attribute_name)
            if self.is_command(attribute):
                subparser = self.subparsers.add_parser(
                    attribute_name,
                    description=attribute.Command.__doc__,
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                )
                attribute.Command.prepare_argparser(subparser)

        self.args, self.remaining_args = self.argparser.parse_known_args(self.raw_args)

    def prepare_command(self):
        command_module = getattr(self.registry, self.command_name, None)
        if self.is_command(command_module):
            return command_module.Command(
                args=self.args,
                remaining_args=self.remaining_args,
                argparser=self.argparser
            )
        raise CommandNotFound('Command with name "{}" was not found'.format(self.command_name))

    def run(self):
        command = self.prepare_command()
        return command.run()

    @staticmethod
    def is_command(command):
        return (
            command and
            hasattr(command, 'Command') and
            inspect.isclass(command.Command) and
            issubclass(command.Command, BaseCommand)
        )
