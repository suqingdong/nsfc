import json


def parse(infile):
    with open(infile) as f:
        for line in f:
            context = json.loads(line.strip())
            if 'project_id' in context:
                yield context
            else:
                data = {}
                data['project_id'] = context['项目编号']
                data['person'] = context['负责人']
                data['institution'] = context['单位']
                data['money'] = context['金额 (万)']
                data['subject'] = context['所属学部']
                data['project_type'] = context['项目类型']
                data['approval_year'] = context['批准年份']
                data['title'] = context['题目']
                data['subject_class_list'] = context['学科分类']
                data['subject_code_list'] = context['学科代码']

                data['subject_code'] = context['学科代码'].split()[-1]

                start, end = context['执行时间'].split(' 至 ')
                data['start_time'] = start.replace('-', '')
                data['end_time'] = end.replace('-', '')

                yield data
