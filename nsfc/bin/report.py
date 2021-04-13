import os
import shutil
import tempfile

import click

from nsfc.src.official import Official


__epilog__ = click.style('''

\b
examples:
    nsfc report 20671004
    nsfc report 20671004 -o out.pdf
    nsfc report 20671004 -o out.pdf --delete
''', fg='yellow')

@click.command(name='report',
               epilog=__epilog__,
               no_args_is_help=True,
               help='download the conclusion report for given project_id')
@click.argument('project_id')
@click.option('-t', '--tmpdir', help='the temporary directory to store pngs', default=tempfile.gettempdir(), show_default=True)
@click.option('-o', '--outfile', help='the output filename of pdf')
@click.option('-k', '--keep', help='do not the temporary directory after completion', is_flag=True)
def main(**kwargs):
    
    tmpdir = tempfile.mktemp(prefix='nsfc-report-', dir=kwargs['tmpdir'])
    if Official.get_conclusion_report(kwargs['project_id'], tmpdir=tmpdir, outfile=kwargs['outfile']):
        if not kwargs['keep']:
            shutil.rmtree(tmpdir)
            Official.logger.debug(f'tempdir deleted: {tmpdir}')


if __name__ == "__main__":
    main()
