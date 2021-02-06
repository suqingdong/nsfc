from webrequests import WebRequest as WR


class Official(object):
    base_url = 'http://output.nsfc.gov.cn'

    field_codes = WR.get_response(base_url + '/common/data/fieldCode').json()['data']

    @classmethod
    def get_field_codes(cls):
        """
            所有的学科代码
        """
        url = cls.base_url + '/common/data/fieldCode'
        print(url)
        return WR.get_response(url).json()['data']

    @classmethod
    def list_root_codes(cls):
        """
            获取所有的学科分类代码
        """
        root_codes = {}
        for context in cls.field_codes:
            if len(context['code']) == 1:
                root_codes[context['code']] = context['name']
        return root_codes

    @classmethod
    def list_child_codes(cls, keys):
        """
            获取最低级的学科代码
                C01  -->  C010101, C010102, ...
                H10  -->  H1001, H1002, ...
        """
        child_codes = {}
        for key in keys.split(','):
            for context in cls.field_codes:
                code = context['code']
                if len(code) == 1:
                    continue
                if code.startswith(key):
                    child_codes[code] = context['name']
                    if code[:-2] in child_codes:
                        del child_codes[code[:-2]]
        return child_codes

    @classmethod
    def get_conclusion_data(cls, ratify_number, detail=True):
        """
            获取指定项目批准号的结题数据
        """
        url = cls.base_url + '/baseQuery/data/conclusionQueryResultsData'
        payload = {
            'ratifyNo': ratify_number,
            'queryType': 'input',
            'complete': 'true',
        }
        result = WR.get_response(url, method='POST', json=payload).json()['data']['resultsData']
        data = {}
        if result:
            data['projectid'] = result[0][0]
            data['project_type'] = result[0][3]
            data['result_stat'] = result[0][10]

        if detail and data.get('projectid'):
            detail_data = cls.get_detail_data(data['projectid'])
            data.update(detail_data)
        return data

    @classmethod
    def get_detail_data(cls, projectid):
        url = cls.base_url + '/baseQuery/data/conclusionProjectInfo/' + projectid
        print(url)
        data = WR.get_response(url).json()['data']
        return data


if __name__ == '__main__':
    import pprint
    # pprint.pprint(Official.list_root_codes())
    # pprint.pprint(Official.list_child_codes('A01'))
    # pprint.pprint(Official.list_child_codes('H'))
    pprint.pprint(Official.get_conclusion_data('11571017'))
    # pprint.pprint(Official.get_conclusion_data('11571017x'))
