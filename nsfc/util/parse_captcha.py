# -*- coding=utf-8 -*-
"""
    验证码识别：
        - 转RGB色彩模式
        - 获取每个点的RGB值，根据条件进行颜色(红色)替换
        - pytesseract识别，长度不为4时重新执行
"""
import io

import click
import pytesseract
from PIL import Image

from webrequests import WebRequest

from nsfc import util


def get_captcha(session, captcha_url):
    
    resp = WebRequest.get_response(captcha_url, session=session)
    im = Image.open(io.BytesIO(resp.content))

    im = im.convert('RGB')

    pixdata = im.load()
    weight, height = im.size
    for x in range(weight):
        for y in range(height):
            rgb = pixdata[x, y]
            if (rgb[0] - rgb[1] > 73) and (rgb[0] - rgb[2] > 73):
                pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)

    captcha = pytesseract.image_to_string(im).strip()

    if len(captcha) != 4:
        return get_captcha(session, captcha_url)

    payload = util.query_payload(tryCode=captcha)
    funding_url = 'http://output.nsfc.gov.cn/baseQuery/data/supportQueryResultsData'
    resp = WebRequest.get_response(funding_url, method='POST', session=session, json=payload)

    if resp.json()['message'] != '验证码错误':
        click.secho('right captcha: {}'.format(captcha), fg='green', bold=True)
        return captcha
    
    click.secho('wrong captcha: {}'.format(captcha), fg='yellow')
    return get_captcha(session, captcha_url)
