import re
import math

from webrequests import WebRequest as WR



class MedSCI(object):
    url = 'https://www.medsci.cn/sci/nsfc.do'

    @classmethod
    def search(cls, page=1, text='', project='', date_begin='', date_end=''):
        params = {
            'txtitle': text,
            'page': page,
            'project_classname_list': project,
            'cost_begin': '',
            'cost_end': '',
            'date_begin': date_begin,
            'date_end': date_end,
            'sort_type': '3',
        }
        soup = WR.get_soup(cls.url, params=params)
        total_count = int(re.findall(r'\d+', soup.select_one('.list-result').text)[0])
        total_page = math.ceil(total_count / 15.)
        print(f'total page: {total_page}, total count: {total_count}')
        if total_count == 500:
            print('too many results: {}'.format(params))
            exit(1)

        for page in range(1, total_page + 1):
            print(f'>>> crawling page: {page}')
            params['page'] = page
            soup = WR.get_soup(cls.url, params=params)
            for a in soup.select('#journalList .journal-item strong a'):
                print(a)
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


if __name__ == '__main__':
    from pprint import pprint

    for each in MedSCI.search(date_begin=2020, date_end=2020):
        pprint(each)
