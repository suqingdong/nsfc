import re
import sys
import math
import json

import click
from webrequests import WebRequest as WR



class MedSCI(object):
    url = 'https://www.medsci.cn/sci/nsfc.do'

    @classmethod
    def search(cls, page=1, txtitle='', project_classname_list='', date_begin='', date_end='', **kwargs):
        params = {
            'txtitle': txtitle,
            'page': page,
            'project_classname_list': project_classname_list,
            'cost_begin': '',
            'cost_end': '',
            'date_begin': date_begin,
            'date_end': date_end,
            'sort_type': '3',
        }
        soup = WR.get_soup(cls.url, params=params)
        total_count = int(re.findall(r'\d+', soup.select_one('.list-result').text)[0])
        total_page = math.ceil(total_count / 15.)
        click.secho(f'total page: {total_page}, total count: {total_count}', err=True, fg='yellow')

        if total_count == 500:
            click.secho(f'too many results: {params}, searching by each project ...', err=True, fg='yellow')
            for project in cls.list_projects():
                if params['project_classname_list']:
                    click.secho(f'still too many results: {params} ...', err=True, fg='red')
                    exit(1)
                params['project_classname_list'] = project
                yield from cls.search(**params)

        for page in range(1, total_page + 1):
            click.secho(f'>>> crawling page: {page}/{total_page}', err=True, fg='green')
            params['page'] = page
            soup = WR.get_soup(cls.url, params=params)
            for a in soup.select('#journalList .journal-item strong a'):
                click.secho(str(a), err=True, fg='white')
                context = {}
                href = a.attrs['href']
                data = dict(list(cls.get_detail(href)))
                context['title'] = data['项目名称']
                context['project_id'] = data['项目批准号']
                context['project_type'] = data['资助类型']
                context['person'] = data['负责人']
                context['institution'] = data['依托单位']
                context['money'] = data['批准金额'].strip('万元')
                context['approval_year'] = data['批准年份']

                context['subject_code'] = data['学科分类'].split()[0]

                context['start_time'], context['end_time'] = data['起止时间'].split('-')

                yield context

    @classmethod
    def get_detail(cls, url):
        soup = WR.get_soup(url)
        for column in soup.select('.journal-content .journal-content-column'):
            key = column.select_one('.column-label').text
            value = column.select_one('.font-black').text.strip()
            yield key, value

    @classmethod
    def list_projects(cls):
        soup = WR.get_soup(cls.url)
        for box in soup.select('.input-area .ms-checkbox input'):
            yield box.attrs['value']


@click.command()
@click.option('-y', '--year', help='the year of approval')
@click.option('-o', '--outfile', help='the output filename')
def main(**kwargs):
    year = kwargs['year']
    out = open(kwargs['outfile'], 'w') if kwargs['outfile'] else sys.stdout

    with out:
        for context in MedSCI.search(date_begin=year, date_end=year):
            out.write(json.dumps(context, ensure_ascii=False) + '\n')
            # break


if __name__ == '__main__':
    main()
