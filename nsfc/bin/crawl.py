import os
import time
import json

import click
from simple_loggers import SimpleLogger

from nsfc.src.letpub import LetPub


@click.command(no_args_is_help=True, name='crawl', help='crawl data from website')
@click.option('-y', '--year', help='the start year of searching', required=True)
@click.option('-e', '--end', help='the end year of searching')
@click.option('-sc', '--subcategory', help='subcategory of searching')
@click.option('-c', '--code', help='the code of subject', required=True)
@click.option('-O', '--outdir', help='the output directory', default='done', show_default=True)
@click.option('-o', '--outfile', help='the output file', default='out.jl', show_default=True)
@click.option('-l', '--level', help='the level of given code', type=click.Choice(['0', '1', '2', '3', '-1']))
@click.option('-L', '--list', help='list the subcode for given code', is_flag=True)
@click.option('-C', '--count', help='count only', is_flag=True)
def main(**kwargs):
    start_time = time.time()

    logger = SimpleLogger('MAIN')
    logger.info(f'input arguments: {kwargs}')

    year = kwargs['year']
    end = kwargs['end'] or year
    code = kwargs['code']
    subcategory = kwargs['subcategory']
    level = int (kwargs['level']) if kwargs['level'] else None
    count = kwargs['count']
    letpub = LetPub(logger=logger)

    outdir = kwargs['outdir']
    outfile = os.path.join(kwargs['outdir'], kwargs['outfile'])
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if kwargs['list']:
        code_list = letpub.code_list
        print(code_list.get(code))
        exit(0)

    try:
        with open(outfile, 'w') as out:
            for context in letpub.search(code, startTime=year, endTime=end, subcategory=subcategory, level=level, count=count):
                if not count:
                    line = json.dumps(context, ensure_ascii=False) + '\n'
                    out.write(line)
        if not count:
            logger.info(f'save file: {outfile}')
    except KeyboardInterrupt:
        os.remove(outfile)

    elapsed = time.time() - start_time
    logger.info(f'elapsed time: {elapsed:.2f}s')


if __name__ == '__main__':
    main()
