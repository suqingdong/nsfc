import os
import sys
import json

import click
from simple_loggers import SimpleLogger

from nsfc.db.model import Project
from nsfc.db.manager import Manager
from nsfc import DEFAULT_DB


@click.command(no_args_is_help=True, name='query', help='query data from the local database')
@click.option('-d', '--dbfile', help='the database file', default=DEFAULT_DB, show_default=True)

@click.option('-s', '--search', help='the search string, eg. project_id 41950410575', multiple=True, nargs=2)

@click.option('-o', '--outfile', help='the output filename')

@click.option('-F', '--format', help='the format of output',
              type=click.Choice(['json', 'jl', 'tsv']), default='jl',
              show_choices=True, show_default=True)
@click.option('-C', '--count', help='just output the out of searching', is_flag=True)
@click.option('-L', '--limit', help='the count of limit of output', type=int)
@click.option('-l', '--log-level', help='the level of logging',
              type=click.Choice(SimpleLogger().level_maps), default='info',
              show_choices=True, show_default=True)
def main(**kwargs):

    logger = SimpleLogger('QUERY')
    logger.level = logger.level_maps[kwargs['log_level']]

    logger.info(f'input arguments: {kwargs}')

    dbfile = kwargs['dbfile']
    limit = kwargs['limit']
    outfile = kwargs['outfile']

    if not os.path.isfile(dbfile):
        logger.error(f'dbfile not exists! [{dbfile}]')
        exit(1)

    uri = f'sqlite:///{dbfile}'
    with Manager(uri=uri, echo=False, logger=logger) as m:

        query = m.session.query(Project)

        if kwargs['search']:
            for key, value in kwargs['search']:
                if '%' in value:
                    query = query.filter(Project.__dict__[key].like(value))
                elif key in ('approval_year', ) and not value.isdigit():
                    if '-' in value:
                        min_value, max_value = value.split('-')
                        query = query.filter(Project.__dict__[key] >= min_value)
                        query = query.filter(Project.__dict__[key] <= max_value)
                    else:
                        logger.error('bad approval_year: {value}')
                        exit(1)
                else:
                    query = query.filter(Project.__dict__[key] == value)

        if limit:
            query = query.limit(limit)

        logger.debug(str(query))

        if kwargs['count']:
            logger.info(f'count: {query.count()}')
        elif not query.count():
            logger.warning('no result for your input')
        else:
            out = open(outfile, 'w') if outfile else sys.stdout
            with out:
                if kwargs['format'] == 'json':
                    data = [{k: v for k, v in row.__dict__.items() if k != '_sa_instance_state'} for row in query]
                    out.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
                else:
                    for n, row in enumerate(query):
                        context = {k: v for k, v in row.__dict__.items() if k != '_sa_instance_state'}
                        if n == 0 and kwargs['format'] == 'tsv':
                            title = '\t'.join(context.keys())
                            out.write(title + '\n')
                        if kwargs['format'] == 'tsv':
                            line = '\t'.join(map(str, context.values()))
                        else:
                            line = json.dumps(context, ensure_ascii=False)
                        out.write(line + '\n')


if __name__ == '__main__':
    main()
