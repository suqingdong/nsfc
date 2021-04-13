import click

from nsfc import version_info
from nsfc.bin.crawl import main as crawl_cli
from nsfc.bin.build import main as build_cli
from nsfc.bin.query import main as query_cli
from nsfc.bin.report import main as report_cli


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

__epilog__ = click.style(f'''\
contact: {version_info['author']} <{version_info['author_email']}>
''', fg='cyan')

@click.group(help=click.style(version_info['desc'], bold=True, fg='green'),
             epilog=__epilog__,
             context_settings=CONTEXT_SETTINGS)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
def cli(**kwargs):
    pass


def main():
    cli.add_command(crawl_cli)
    cli.add_command(build_cli)
    cli.add_command(query_cli)
    cli.add_command(report_cli)
    cli()


if __name__ == '__main__':
    main()
