import os
import json

import click

from nsfc.src.letpub import LetPub
from nsfc.src.official import Official

from nsfc.db.model import Project
from nsfc.db.manager import Manager
from nsfc.util.parse_data import parse


@click.command()
@click.option('-y', '--year', help='the year of searching', required=True)
@click.option('-c', '--code', help='the code of subject', required=True)
@click.option('-O', '--outdir', help='the output directory')
@click.option('-s', '--special', help='search with special', type=int)
@click.option('-S', '--special2', help='search with special2', is_flag=True)
def main(**kwargs):
    year = kwargs['year']
    code = kwargs['code']
    special = kwargs['special']
    special2 = kwargs['special2']
    letpub = LetPub()
    outdir = kwargs['outdir'] or os.path.join('done', code[0], str(year))
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    done = {each.rsplit('.', 1)[0]: 1 for each in os.listdir(outdir)}

    code_list = letpub.list_codes

    for code in sorted(code_list[code]):
        print(done)
        if special == 3:
            code = code[:3]
            done = {each.rsplit('.', 1)[0]: 1 for each in os.listdir(outdir)}
        elif special == 2:
            code = code[:5]
            done = {each.rsplit('.', 1)[0]: 1 for each in os.listdir(outdir)}

        if f'{code}.{year}' in done:
            continue

        outfile = f'{outdir}/{code}.{year}.jl'
        try:
            with open(outfile, 'w') as out:
                for context in letpub.search(code_list, code, start_year=year, end_year=year, special=special, special2=special2):
                    line = json.dumps(context, ensure_ascii=False) + '\n'
                    out.write(line)
            click.secho(f'save file: {outfile}')
        except KeyboardInterrupt:
            os.remove(outfile)
            break


if __name__ == '__main__':
    main()
