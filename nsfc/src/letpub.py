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
        self.province_list = self.list_provinces()

    def list_support_types(self):
        """项目类别列表

            Bug: 网页显示：应急管理项目
                 实际应该：科学部主任基金项目/应急管理项目
        """
        soup = WR.get_soup(self.index_url)
        options = soup.select('select#subcategory option')
        subcategory_list = [option.text for option in options[1:]]
        return subcategory_list
    
    def list_provinces(self):
        """省份列表
        """
        soup = WR.get_soup(self.index_url)
        province_list = [each.attrs['value'] for each in soup.select('#province_main option[value!=""]')]
        return province_list

    def search(self, code_list, code, page=1, start_year='', end_year='', subcategory='', special=False, special2=False, province_main=''):
        """项目查询，最多显示20页(200条)，超出时增加项目类别细分查询

            special==2: 特殊情况， 二级 == 三级           A02 A0203 A0203
            special==3: 特殊情况， 一级 == 二级 == 三级   A01 A01 A01
            special2: special基础上，结果大于200
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
            'province_main': province_main,
        }

        if special == 3:
            for level in range(2, 5):
                payload[f'addcomment_s{level}'] = code[:3]
        elif special == 2:
            payload['addcomment_s2'] = code[:3]
            for level in range(3, 5):
                payload[f'addcomment_s{level}'] = code[:5]
        else:
            level = math.ceil(len(code) / 2.)
            payload[f'addcomment_s{level}'] = code

        soup = self.search_page(params, payload)
        total_count = int(soup.select_one('#dict div b').text)
        total_page = math.ceil(total_count / 10.)

        if special==3 and special2 and total_page <= 20 and (not province_main):
            print(f'*** skip special=={special}: {total_count}: {payload}')
        else:
            print('total count: {} [{}]'.format(total_count, payload))
            if 0 < total_page <= 20:
                print(f'>>> dealing with page: {page}/{total_page} [{payload}]')
                yield from self.parse_content(soup)
                if page < total_page:
                    page += 1
                    yield from self.search(code_list, code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory, special=special, special2=special2, province_main=province_main)
            elif total_page > 20:
                if special:
                    print('too many result, search with province ...')
                    for province_main in self.province_list:
                        yield from self.search(code_list, code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory, special=special, special2=special2, province_main=province_main)
                elif not subcategory:
                    print('too many result, search with subcategory ...')
                    for subcategory in self.subcategory_list:
                        yield from self.search(code_list, code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory, special=special, special2=special2, province_main=province_main)
                else:
                    print('too many result, search with subcategory and subclass ...')
                    for subcategory in self.subcategory_list:
                        for code2 in code_list[code[0]][code]:
                            if code2 != code:
                                yield from self.search(code_list, code2, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory, special=special, special2=special2, province_main=province_main)

            # if page < total_page:
            #     page += 1
            #     yield from self.search(code_list, code, page=page, start_year=start_year, end_year=end_year, subcategory=subcategory, special=special, special2=special2, province_main=province_main)

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
    import json
    from pprint import pprint

    letpub = LetPub()
    code_list = letpub.list_codes

    # for code in sorted(code_list.get('A')):
    #     print(code)
    #     print(sorted(code_list['A'][code]))

    # for context in letpub.search(code_list, 'E0805', start_year=2016, end_year=2016):
    #     print(context)

    # for context in letpub.search(code_list, 'A03', start_year=1997, end_year=1997, special=True):
    #     print(context)

    with open('out.jl', 'w') as out:
        for context in letpub.search(code_list, 'A0203', start_year=2019, end_year=2019, special=2, special2=False):
            # print(context)
            out.write(json.dumps(context, ensure_ascii=False) + '\n')
