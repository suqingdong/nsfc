#!/usr/bin/env python
# -*- coding=utf-8 -*-
import click

from nsfc import util, NSFC, __version__, __author__, __author_email__
from nsfc.util.export import Export


__epilog__ = '''
contact: {__author__} <{__author_email__}>
'''.format(**locals())


__search_examples__ = '''

# 1 运行时选择申请代码和批准年度

nsfc search

# 2 指定申请代码和批准年度，多个值之间可用逗号分隔

nsfc search -c C05,C06 -y 2018,2019,2020

# 3 指定查询类型(Z: 资助项目[默认]，J: 结题项目)

nsfc search -c C05,C06 -y 2018,2019,2020 -t J

# 4 指定输出文件和格式(html, xlsx, txt/tsv, json, jl, pkl)

nsfc search -c C05 -y 2019 -o out [默认 -O xlsx]

nsfc search -c C05 -y 2019 -o out -O html

nsfc search -c C05 -y 2019 -o out -O tsv

nsfc search -c C05 -y 2019 -o out -O json

nsfc search -c C05 -y 2019 -o out -O jl
'''


@click.group(epilog=__epilog__, help=click.style('国家自然科学基金查询系统', fg='green', bold=True))
@click.version_option(version=__version__, prog_name='nsfc')
def cli():
    pass


@cli.command(help=click.style('查看申请/资助类别代码', fg='cyan', bold=True))
@click.option('-t', '--types', help='S: 申请代码， Z: 资助类别', type=click.Choice('SZ'))
def show_codes(types):
    types = types or click.prompt(
        '请输入要查看的内容： S - 申请代码， Z - 资助类别', type=click.Choice('SZ'))
    nsfc = NSFC()
    if types == 'S':
        util.show_table(nsfc.field_codes, fields=['name', 'code'])
    else:
        util.show_table(nsfc.support_types, fields=['name', 'value'])


@cli.command(help=click.style('资助/结题项目查询', fg='yellow', bold=True), epilog=__search_examples__)
@click.option('-c', '--codes', help='申请(学科)代码')
@click.option('-y', '--years', help='年度')
@click.option('-p', '--projects', help='资助类别(代码)')
@click.option('-o', '--outfile', help='输出文件名前缀', default='nsfc', show_default=True)
@click.option('-O', '--outtype', help='输出文件格式', default='xlsx', show_default=True, type=click.Choice('html xlsx tsv txt json jl pkl all'.split()))
@click.option('-t', '--type', help='查询类型：Z - 资助项目，J - 结题项目', type=click.Choice('ZJ'), default='Z', show_default=True)
def search(**kwargs):
    nsfc = NSFC()

    nsfc.logger.debug('input arguments: {}'.format(kwargs))

    projects = kwargs['projects'].split(',') if kwargs['projects'] else [
        each['value'] for each in nsfc.support_types]
    years = kwargs['years'].split(
        ',') if kwargs['years'] else click.prompt('请输入批准年度').split(',')
    child_codes = nsfc.get_child_codes(
        kwargs['codes'] or click.prompt('请输入申请代码'))

    out_data = []
    for code in child_codes:
        for year in years:
            for project in projects:
                nsfc.logger.debug(
                    '>>> crawling: {} - {} - {}'.format(code, year, project))
                if kwargs['type'] == 'Z':
                    result = nsfc.funding_query(
                        code=code, ratifyYear=year, projectType=project)
                else:
                    result = nsfc.project_query(
                        code=code, conclusionYear=year, projectType=project)
                out_data += [
                    context for context in nsfc.format_context(result)]

    if out_data:
       
        nsfc.logger.info('{} results found.'.format(len(out_data)))

        if kwargs['outtype'] == 'all':
            outtypes = 'html xlsx json jl pkl tsv'.split()
        else:
            outtypes = [kwargs['outtype']]

        for outtype in outtypes:
            outfile = '{}.{}'.format(kwargs['outfile'], outtype)
            if outtype == 'html':
                Export(out_data, outfile).to_html()
            elif outtype == 'xlsx':
                Export(out_data, outfile).to_excel()
            elif outtype == 'json':
                Export(out_data, outfile).to_json()
            elif outtype == 'jl':
                Export(out_data, outfile).to_jsonlines()
            elif outtype == 'pkl':
                Export(out_data, outfile).to_pickle()
            elif outtype in ('tsv', 'txt'):
                Export(out_data, outfile).to_tsv()
            nsfc.logger.info('save file: {}'.format(outfile))
    else:
        nsfc.logger.info('no result for your input.')


if __name__ == '__main__':
    cli()
