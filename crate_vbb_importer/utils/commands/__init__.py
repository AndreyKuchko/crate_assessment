# -*- coding: utf-8 -*-
import sys

from crate_vbb_importer.utils.commands.manager import CommandManager


def run_command(registry):
    """ Single entry point for all commands
    """
    command_manager = CommandManager(registry=registry, raw_args=sys.argv[1:])
    command_manager.init_argparser()
    return command_manager.run()
