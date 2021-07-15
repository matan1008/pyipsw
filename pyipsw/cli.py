import click
from humanfriendly.tables import format_smart_table

from pyipsw.pyipsw import get_devices, DEVICES_FIELDS, get_itunes, ITUNES_FIELDS, download_devices

DEFAULT_DEVICES_COLUMNS = ['device', 'version', 'buildid', 'filename']
DEFAULT_ITUNES_COLUMNS = ['os', 'version', 'releasedate', 'url']


@click.group()
def cli():
    pass


@cli.command()
@click.option('-c', '--columns', type=click.Choice(DEVICES_FIELDS, case_sensitive=False), multiple=True,
              help='Data to show')
@click.option('-f', '--filters', type=click.STRING, default='',
              help='Python code to act as filter to devices, e.g. "iPhone11" in device')
def devices(columns, filters):
    """ Show data about apple devices. """
    if columns == ():
        columns = DEFAULT_DEVICES_COLUMNS
    table_data = [[firmware[key] if key in firmware else '' for key in columns] for firmware in get_devices(filters)]
    print(format_smart_table(table_data, columns))


@cli.command('download-devices')
@click.argument('out_directory', type=click.Path(exists=True, file_okay=False))
@click.option('-f', '--filters', type=click.STRING, default='',
              help='Python code to act as filter to devices, e.g. "iPhone11" in device')
def download_devices_cli(out_directory, filters):
    """ Download apple devices firmwares. """
    download_devices(out_directory, filters)


@cli.command()
@click.option('-c', '--columns', type=click.Choice(ITUNES_FIELDS, case_sensitive=False), multiple=True,
              help='Data to show')
@click.option('-f', '--filters', type=click.STRING, default='',
              help='Python code to act as filter to itunes, e.g. "Windows" == os')
def itunes(columns, filters):
    """ Show data about iTunes versions. """
    if columns == ():
        columns = DEFAULT_ITUNES_COLUMNS
    table_data = [[version[key] if key in version else '' for key in columns] for version in get_itunes(filters)]
    print(format_smart_table(table_data, columns))
