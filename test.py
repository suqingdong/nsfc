from webrequests import WebRequest as WR


url = 'http://www.letpub.com.cn/nsfcfund_search.php'


params = {
    'mode': 'advanced',
    'datakind': 'list',
    'currentpage': 1
}

payload = {
    'addcomment_s1': 'A',
    # 'addcomment_s2': 'A01',
    # 'addcomment_s3': 'A0101',
    'addcomment_s4': 'A010101',
    # 'addcomment_s3': 'H1401',
    'startTime': 2019,
    'endTime': 2020,
    'searchsubmit': 'true',
}


soup = WR.get_soup(url, method='POST', params=params, data=payload)

total = int(soup.select_one('#dict div b').text)
print('total:', total)

trs = soup.select('table.table_yjfx tr')
title = [th.text for th in trs[1].select('th')]

data = []

context = None
for tr in trs[2:-1]:
    if tr.has_attr('style'):
        if context:
            data.append(context)
        row = [td.text for td in tr.select('td')]
        context = dict(zip(title, row))
    else:
        row = [td.text for td in tr.select('td')]
        context.update(dict([row]))
data.append(context)

print(len(data))
print(data[0])
print(data[-1])
