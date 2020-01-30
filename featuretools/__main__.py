import click
import pandas as pd
import pkg_resources
from packaging import version

import featuretools
from featuretools.utils.cli_utils import print_info


@click.group()
def cli():
    pass


@click.command()
def info():
    print_info()


@click.command(name='list-primitives')
def list_primitives():
    if version.parse(pd.__version__) < version.parse('1.0.0rc0'):
        col_width = -1
    else:
        col_width = None
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', col_width, 'display.width', 1000):
        print(featuretools.list_primitives())


cli.add_command(list_primitives)
cli.add_command(info)

for entry_point in pkg_resources.iter_entry_points('featuretools_cli'):
    try:
        loaded = entry_point.load()
        if hasattr(loaded, 'commands'):
            for name, cmd in loaded.commands.items():
                cli.add_command(cmd=cmd, name=name)
    except Exception:
        pass

if __name__ == "__main__":
    cli()
