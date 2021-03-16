import re
import math
import time
import random
from collections import defaultdict

from webrequests import WebRequest as WR


class LetPub(object):
    base_url = 'http://www.letpub.com.cn'
    index_url = base_url + '/index.php?page=grant'
    search_url = base_url + '/nsfcfund_search.php'

    def __init__(self):
        self.subcategory_list = self.list_support_types()

    def list_support_types(self):
        """项目类别列表
        """
        soup = WR.get_soup(self.index_url)
        options = soup.select('select#subcategory option')
        subcategory_list = [option.text for option in options[1:]]
        return subcategory_list
    

    def search(self, code_list, code, page=1, start_year='', end_year='', subcategory='', special=False):
        """项目查询，最多显示20页(200条)，超出时增加项目类别细分查询

            special: 特殊情况，例如一级，二级，三级学科都是A01的情况
        """
        params = {
            'mode': 'advanced',
            'datakind': 'list',
            'currentpage': page
        }

        payload = {
            'addcomment_s1': code[0],
            'startTime': start_year,
            'endTime': end_year,
            'searchsubmit': 'true',
            'subcategory': subcategory,
        }

        if special:
            for level in range(2, 5):
                payload['addcomment_s{}'.format(level)] = code[:3]
        else:
            level = math.ceil(len(code) / 2.)
            payload.update({
                'addcomment_s{}'.format(level): code
            })

        soup = self.search_page(params, payload)
        total_count = int(soup.select_one('#dict div b').text)
        total_page = math.ceil(total_count / 10.)

        print('total count: {} [{}]'.format(total_count, payload))
        if 0 < total_page <= 20:
            print('>>> dealing with page: {}/{} [{}]'.format(page, total_page, payload))
            yield from self.parse_content(soup)
        elif total_page > 20:
            if not subcategory:
                print('too many result, search with subcategory ...')
                for subcategory in self.subcategory_list:
                    yield from self.search(code_list, code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory, special=special)
            else:
                print('too many result, search with subcategory and subclass ...')
                for subcategory in self.subcategory_list:
                    for code2 in code_list[code[0]][code]:
                        if code2 != code:
                            yield from self.search(code_list, code2, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory, special=special)

        if page < total_page:
            page += 1
            yield from self.search(code_list, code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory)

    def parse_content(self, soup):
        """项目内容解析
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

    def search_page(self, params, payload):
        """查询页面
        """
        while True:
            soup = WR.get_soup(self.search_url, method='POST', params=params, data=payload)
            if not soup.select_one('#dict div b'):
                print('*****', soup.text)
                time.sleep(30)
                continue
            time.sleep(random.randint(5, 10))
            return soup

    @property
    def list_codes(self):
        url = self.base_url + '/js/nsfctags2019multiple.js'
        resp = WR.get_response(url)
        codes = {}
        for line in resp.text.split('\n'):
            if line.startswith('subtag['):
                linelist = line.strip().split("', '")

                code = linelist[4]  # 二级学科  A01
                code2 = linelist[5]  # 三级学科 A0101 

                if len(code) != 5:
                    continue

                if code[0] not in codes:
                    codes[code[0]] = defaultdict(set)

                codes[code[0]][code].add(code2)

        return codes


if __name__ == '__main__':
    from pprint import pprint

    letpub = LetPub()
    code_list = letpub.list_codes

    # for code in sorted(code_list.get('A')):
    #     print(code)
    #     print(sorted(code_list['A'][code]))

    # for context in letpub.search(code_list, 'E0805', start_year=2016, end_year=2016):
    #     print(context)

    for context in letpub.search(code_list, 'A03', start_year=1997, end_year=1997, special=True):
        print(context)
