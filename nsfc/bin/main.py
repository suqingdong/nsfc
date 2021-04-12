import click

from nsfc import version_info
from nsfc.bin.crawl import main as crawl_cli
from nsfc.bin.build import main as build_cli
from nsfc.bin.query import main as query_cli


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(help=version_info['desc'], context_settings=CONTEXT_SETTINGS)
@click.version_option(version=version_info['version'])
def cli(**kwargs):
    pass


def main():
    cli.add_command(crawl_cli)
    cli.add_command(build_cli)
    cli.add_command(query_cli)
    cli()



if __name__ == '__main__':
    main()
