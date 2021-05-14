# -*- coding: utf-8; -*-
from crate_vbb_importer import commands
from crate_vbb_importer.utils.commands import run_command


def entry_point():
    run_command(registry=commands)


if __name__ == '__main__':
    entry_point()
