import math
import time
import random
from collections import defaultdict

import requests
from webrequests import WebRequest as WR
from simple_loggers import SimpleLogger

"""
注意事项：
- 查询结果最多显示20页(200个条目)
- 按学科查询时，会存在特殊情况：
    - 2级 == 3级           eg. A02 A0203 A0203
    - 1级 == 2级 == 3级    eg. A01 A01 A01
- 按项目类别查询时，"应急管理项目" 实际应该为 "科学部主任基金项目/应急管理项目"

其他问题：
- 列表文件应该是旧的，数据不全
- 存在列表中没有的学科，如A06, A08 （U1930117）
- 或学科编号和官网不一致：eg. 11571001
    - LetPub: A011404
    - 官网：A0602 (http://output.nsfc.gov.cn/conclusionProject/2672d6fe408220c02da8ab9e24a0f637)
- 列表中没有其他学部(L)

"""


class LetPub(object):
    base_url = 'http://www.letpub.com.cn'
    index_url = base_url + '/index.php?page=grant'
    search_url = base_url + '/nsfcfund_search.php'

    def __init__(self, logger=None):
        self.logger = logger or SimpleLogger('LetPub')
        self.subcategory_list = self.list_support_types()
        self.province_list = self.list_provinces()
        self.code_list = self.list_codes()

    def list_support_types(self):
        """项目类别列表

            Bug: 网页显示：应急管理项目
                 实际应该：科学部主任基金项目/应急管理项目
        """
        self.logger.debug('list support types ...')
        soup = WR.get_soup(self.index_url)
        subcategory_list = []
        for option in soup.select('select#subcategory option')[1:]:
            if option.text == '应急管理项目':
                text = '科学部主任基金项目/应急管理项目'
            else:
                text = option.text
            subcategory_list.append(text)

        return subcategory_list
    
    def list_provinces(self):
        """省份列表
        """
        self.logger.debug('list provinces ...')
        soup = WR.get_soup(self.index_url)
        province_list = [each.attrs['value'] for each in soup.select('#province_main option[value!=""]')]
        return province_list

    def list_codes(self):
        self.logger.debug('list subject codes ...')
        url = self.base_url + '/js/nsfctags2019multiple.js'
        resp = WR.get_response(url)

        codes = defaultdict(list)
        for line in resp.text.split('\n'):
            if line.startswith('subtag['):
                linelist = line.strip().split("', '")
                subject = linelist[2]                   # 学部
                code1 = linelist[3]                     # 一级学科 A01
                code2 = linelist[4]                     # 二级学科 A0101 
                code3 = linelist[5]                     # 二级学科 A010101
                # name = linelist[6].split("'")[0]        # 学科名字

                if code1 not in codes[subject]:
                    codes[subject].append(code1)
                if code2 not in codes[code1]:
                    codes[code1].append(code2)
                if code3 not in codes[code2]:
                    codes[code2].append(code3)

                # print(subject, name, code1, code2, code3)
        return dict(codes)

    def search(self, code, page=1, startTime='', endTime='', subcategory='', province_main='', level='', count=False):
        params = {
            'mode': 'advanced',
            'datakind': 'list',
            'currentpage': page
        }
        payload = {
            'addcomment_s1': code[0],
            'startTime': startTime,
            'endTime': endTime,
            'subcategory': subcategory,
            'province_main': province_main,
        }

        level = level or int((len(code) - 1) / 2)
        if level > 0:
            payload[f'addcomment_s{level+1}'] = code

        soup = self.search_page(params, payload)
        total_count = int(soup.select_one('#dict div b').text)
        total_page = math.ceil(total_count / 10.)
        self.logger.info(f'total count: {total_count} [{payload}]')

        if count:
            yield None
        elif total_page > 20:
            if 0 <= level < 3 and code in self.code_list:
                self.logger.warning(f'too many results, search with class level: {level+1} ...')
                for code2 in self.code_list[code]:
                    yield from self.search(code2, page=page, startTime=startTime, endTime=endTime, subcategory=subcategory, province_main=province_main, level=level+1)
            elif not subcategory:
                self.logger.warning('too many results, search with subcategory ...')
                for subcategory in self.subcategory_list:
                    yield from self.search(code, page=page, startTime=startTime, endTime=endTime, subcategory=subcategory, province_main=province_main, level=level)
            elif not province_main:
                self.logger.warning('too many results, search with province_main ...')
                for province_main in self.province_list:
                    yield from self.search(code, page=page, startTime=startTime, endTime=endTime, subcategory=subcategory, province_main=province_main, level=level)
            else:
                self.logger.error(f'still too many results! [{payload}]')
        elif total_page > 0:
            self.logger.debug(f'parsing for page: {page}/{total_page}')
            yield from self.parse_page(soup)
            if page < total_page:
                page += 1
                yield from self.search(code, page=page, startTime=startTime, endTime=endTime, subcategory=subcategory, province_main=province_main, level=level)
            # yield code, total_count

    def search_page(self, params, payload):
        """查询页面
        """
        self.logger.debug(f'searching for: {payload} [page: {params["currentpage"]}]')
        while True:
            soup = WR.get_soup(self.search_url, method='POST', params=params, data=payload)
            if not soup.select_one('#dict div b'):
                self.logger.warning(f'{soup.text}')
                if '需要先注册登录' in soup.text:
                    exit()
                time.sleep(30)
                continue

            time.sleep(random.randint(5, 10))
            return soup

    def parse_page(self, soup):
        """项目内容列表解析
        """
        ths = soup.select('table.table_yjfx .table_yjfx_th')
        if ths:
            title = [th.text for th in ths]
            context = {}
            for tr in soup.select('table.table_yjfx tr')[2:-1]:
                values = [td.text for td in tr.select('td')]
                if len(values) == len(title):
                    if context:
                        yield context
                    context = dict(zip(title, values))
                else:
                    context.update(dict([values]))
            yield context


if __name__ == '__main__':
    import json
    from pprint import pprint

    # letpub = LetPub(logfile='run.log')
    letpub = LetPub()
    old_codes = [k for k in letpub.code_list.keys() if len(k)==3]


    url = 'http://output.nsfc.gov.cn/common/data/fieldCode'
    # data = requests.get(url).json()['data']
    # new_codes = []
    # for item in data:
    #     code = item['code']
    #     if len(code) == 3 and code not in old_codes:
    #         new_codes.append(code)
    # print(new_codes)
    
    # code = 'A0203'
    # code = 'A26'

    year = 2019
    
    subcategory = ''
    # subcategory = '科学部主任基金项目/应急管理项目'

    # for code in new_codes:
    #     if not code.startswith('A'):
    #         continue
    #     with open(f'{code}.{year}.jl', 'w') as out:
    #         for each in letpub.search(code, startTime=year, endTime=year, subcategory=subcategory):
    #             out.write(json.dumps(each, ensure_ascii=False) + '\n')

    code = 'L'
    year = 2017
    level = -1
    with open(f'{code}.{year}.jl', 'w') as out:
        for each in letpub.search(code, startTime=year, endTime=year, subcategory=subcategory, level=level):
            out.write(json.dumps(each, ensure_ascii=False) + '\n')

