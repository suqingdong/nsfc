import click

from nsfc import version_info
from .crawl import main as crawl_cli
from .build import main as build_cli
from .query import main as query_cli


@click.group(help=version_info['desc'])
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
