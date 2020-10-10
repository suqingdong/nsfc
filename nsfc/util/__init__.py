# -*- coding=utf-8 -*-
import os
import click
import prettytable


def safe_open(filename, mode='r'):
    if 'w' in mode:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return open(filename, mode=mode)



def show_table(data, fields=None):
    """
        Show PrettyTable
    """
    fields = fields or data[0].keys()
    table = prettytable.PrettyTable(['index'] + fields)
    for n, row in enumerate(data, 1):
        table.add_row([n] + list(map(row.get, fields)))
    click.secho(str(table), fg='cyan', bold=True)



def query_payload(**kwargs):
    """
        结题项目检索和资助项目检索，必填和选填参数
    """
    payload = {
        'code': '',               # 申请代码(必填)
        'projectType': '',        # 资助类别(必填)

        'conclusionYear': '',     # 结题年度(结题项目检索，必填)
        'ratifyYear': '',         # 批准年度(资助项目检索，必填)

        'ratifyNo': '',           # 项目批准号
        'projectName': '',        # 项目名称
        'personInCharge': '',     # 项目负责人
        'dependUnit': '',         # 依托单位
        'keywords': '',           # 项目关键词
        'subPType': '',           # 亚类说明
        'psPType': '',            # 附注说明

        'pageNum': 0,
        'pageSize': 10,           # 最大值为10

        'beginYear': '',
        'endYear': '',
        'adminID': '',
        'checkDep': '',
        'checkType': '',
        'quickQueryInput': '',
        'queryType': 'input',

        'complete': '',          # true or false

        'tryCode': '',           # 验证码(资助项目检索，必填)
    }
    payload.update(**kwargs)

    return payload