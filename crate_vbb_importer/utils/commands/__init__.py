# -*- coding: utf-8 -*-
import sys

from crate_vbb_importer.utils.commands.manager import CommandManager


def run_command(registry):
    command_manager = CommandManager(registry=registry, raw_args=sys.argv[1:])
    command_manager.init_argparser()
    # init_logging(settings, logs_basename=command_manager.command_name)
    return command_manager.run()
