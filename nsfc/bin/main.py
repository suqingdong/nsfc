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
def main(**kwargs):
    year = kwargs['year']
    code = kwargs['code']
    letpub = LetPub()
    outdir = kwargs['outdir'] or os.path.join('done', code[0], str(year))
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    done = {each.rsplit('.', 1)[0]: 1 for each in os.listdir(outdir)}

    for code in sorted(letpub.list_codes[code]):
        if f'{code}.{year}' in done:
            continue
        outfile = f'{outdir}/{code}.{year}.jl'
        try:
            with open(outfile, 'w') as out:
                for context in letpub.search(code, start_year=year, end_year=year):
                    line = json.dumps(context, ensure_ascii=False) + '\n'
                    out.write(line)
            click.secho(f'save file: {outfile}')
        except KeyboardInterrupt:
            os.remove(outfile)
            break


if __name__ == '__main__':
    main()

# root_codes = Official.list_root_codes()
# child_codes =  Official.list_child_codes('A')




# done = {each.split('.')[0]: 1 for each in os.listdir('A')}

# year = 2019
# for child in child_codes:
#     if child in done:
#         # print(f'{child} is done')
#         continue
#     with open(f'{child}.{year}.jl', 'w') as out:
#         for context in letpub.search(child, start_year=year, end_year=year):
#             line = json.dumps(context, ensure_ascii=False) + '\n'
#             out.write(line)
