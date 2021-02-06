from pprint import pprint

import click

from nsfc.db.model import Project
from nsfc.db.manager import Manager
from nsfc.src.official import Official
from nsfc.util.parse_data import parse


@click.command()
@click.option('-i', '--infile', help='the input filename', required=True)
@click.option('-d', '--dbfile', help='the path of database file', default='project.db')
@click.option('--echo', help='turn echo on for sqlalchemy', is_flag=True)
@click.option('--drop', help='drop table before creating', is_flag=True)
def build(**kwargs):
    print(kwargs)
    uri = 'sqlite:///{dbfile}'.format(**kwargs)
    with Manager(uri=uri, echo=kwargs['echo'], drop=kwargs['drop']) as m:
        for data in parse(kwargs['infile']):

            query_result = m.query(Project, 'project_id', data['project_id']).first()
            if query_result:
                print('*** skip ***', query_result)
                continue
            
            project = Project(**data)

            conc_data = Official.get_conclusion_data(data['project_id'])
            if conc_data:
                project.finished = True
                project.project_type_code = conc_data.get('projectType')
                project.abstract = conc_data.get('projectAbstractC')
                project.abstract_en = conc_data.get('projectAbstractE')
                project.abstract_conc = conc_data.get('conclusionAbstract')
                project.keyword = conc_data.get('projectKeywordC')
                project.keyword_en = conc_data.get('projectKeywordE')
                project.result_stat = conc_data.get('result_stat')

            pprint(project.as_dict)
            m.insert(Project, 'project_id', project)
            break


if __name__ == '__main__':
    build()
