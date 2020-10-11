#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
    国家自然科学基金查询系统
"""
import sys
import json

from collections import OrderedDict

import click
import requests
import prettytable

from webrequests import WebRequest, SimpleLogger

from nsfc import util
from nsfc.util.export import Export
from nsfc.util.parse_captcha import get_captcha


PY2 = sys.version_info.major == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


__version__ = '1.0.0'
__author__ = 'suqingdong'
__author_email__ = '1078595229@qq.com'


class NSFC(object):
    base_url = 'http://output.nsfc.gov.cn'
    captcha_url = base_url +'/captcha/defaultCaptcha'

    def __init__(self):
        self.session = requests.Session()
        self.captcha = None     # 验证码可重复使用
        self.logger = SimpleLogger('NSFC', level='debug')

    @property
    def support_types(self):
        """
            资助类别
        """
        # url = self.base_url + '/common/data/supportTypeData'        # 包含子类
        url = self.base_url + '/common/data/supportTypeClassOneData'  # 仅一类
        return WebRequest.get_response(url).json()['data']

    @property
    def field_codes(self):
        """
            申请代码
        """
        url = self.base_url + '/common/data/fieldCode'
        return WebRequest.get_response(url).json()['data']

    def get_child_codes(self, keys):
        """
            获取最低级
                C01  -->  C010101, C010102, ...
                H10  -->  H1001, H1002, ...
        """
        child_codes = {}
        for key in keys.split(','):
            for context in self.field_codes:
                code = context['code']
                if len(code) == 1:
                    continue
                if code.startswith(key):
                    child_codes[code] = context['name']
                    if code[:-2] in child_codes:
                        del child_codes[code[:-2]]
        return child_codes

    def do_search(self, url, requires, **kwargs):
        """
        
        """
        if not kwargs.get('ratifyNo'):
            for key, name in requires.items():
                if not kwargs.get(key):
                    kwargs[key] = click.prompt('请输入{}'.format(name))

        
        payload = util.query_payload(**kwargs)

        data = WebRequest.get_response(url, method='POST', json=payload, session=self.session, max_try=20).json()

        if data['code'] != 200:
            print(payload)
            click.secho('error code: {}'.format(json.dumps(data, ensure_ascii=False)), fg='red')
            exit()
            for each in self.do_search(url, requires, **payload):
                yield each
        else:
            yield data
            # 结果大于10条
            total = data['data']['iTotalRecords']
            if (payload['pageNum'] + 1) * payload['pageSize'] < total:
                payload['pageNum'] += 1
                click.secho('>>> crawling {code}-{projectType}-{ratifyYear} page {page} ...'.format(page=payload['pageNum'] + 1, **payload), fg='cyan')
                for each in self.do_search(url, requires, **payload):
                    yield each

    def funding_query(self, **kwargs):
        """
            资助项目检索

            需要验证码

            必填参数
                - ratifyNo      项目批准号
                or
                - code          申请代码
                - projectType   资助类别
                - ratifyYear    批准年度
        """
        url = self.base_url + '/baseQuery/data/supportQueryResultsData'
        requires = {'code': '申请代码', 'projectType': '资助类别', 'ratifyYear': '批准年度'}

        if self.captcha is None:
            self.captcha = get_captcha(self.session, self.captcha_url)

        kwargs['tryCode'] = self.captcha

        return self.do_search(url, requires, **kwargs)

    def project_query(self, **kwargs):
        """
            结题项目检索(包含于资助项目中，用处不大)

            必填参数
                - ratifyNo          项目批准号
                or
                - code              申请代码
                - projectType       资助类别
                - conclusionYear    结题年度
        """
        url = self.base_url + '/baseQuery/data/conclusionQueryResultsData'
        requires = {'code': '申请代码', 'projectType': '资助类别', 'conclusionYear': '结题年度'}
        return self.do_search(url, requires, **kwargs)

    def conclusion_project(self, projectid):
        """
            结题项目详情        
        """
        url = self.base_url + '/baseQuery/data/conclusionProjectInfo/' + projectid
        data = WebRequest.get_response(url).json()['data']
        return data

    def format_context(self, query_result):
        """
            查询结果转成字典
        """
        header = '项目名称 批准号 项目类别 依托单位 项目负责人 资助经费(万元) 批准年度 关键词 是否结题 研究成果(期刊论文;会议论文;著作;奖励;专利) 依托单位ID 项目负责人ID 项目类别代码 申请代码 起止年月'.split()
        context = OrderedDict()

        for each in header:
            context[each] = ''     

        for data in query_result:
            for row in data['data']['resultsData']:
                tmp = dict(zip(header, row[1:]))
                context.update(tmp)

                conclusion_context = {}
                if context['是否结题'] == 'true':
                    conclusion_context = self.conclusion_project(context['批准号'])

                context['中文摘要'] = conclusion_context.get('projectAbstractC', '')
                context['英文摘要'] = conclusion_context.get('projectAbstractE', '')
                # context['结题摘要'] = conclusion_context.get('conclusionAbstract', '')
                context['依托单位ID'] = conclusion_context.get('dependUintID', '')
                context['项目负责人ID'] = conclusion_context.get('projectAdminID', '')
                context['负责人职称'] = conclusion_context.get('adminPosition', '')

                context['是否结题'] = '是' if context['是否结题'] == 'true' else '否'

                yield context


if __name__ == '__main__':
    nsfc = NSFC()
    child_codes = nsfc.get_child_codes('C05,C08')
    print(child_codes)
    