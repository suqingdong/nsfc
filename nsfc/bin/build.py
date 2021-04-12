from pprint import pprint

import click

from nsfc.db.model import Project
from nsfc.db.manager import Manager
from nsfc.src.official import Official
from nsfc.util.parse_data import parse as parse_data
from nsfc import DEFAULT_DB


@click.command(no_args_is_help=True, name='build', help='build the local database')
@click.argument('infiles', nargs=-1)
@click.option('-d', '--dbfile', help='the path of database file', default=DEFAULT_DB, show_default=True)
@click.option('--echo', help='turn echo on for sqlalchemy', is_flag=True)
@click.option('--drop', help='drop table before creating', is_flag=True)
@click.option('-no', help='do not get conclusion data', is_flag=True)
def main(**kwargs):
    print(kwargs)
    uri = 'sqlite:///{dbfile}'.format(**kwargs)
    with Manager(uri=uri, echo=kwargs['echo'], drop=kwargs['drop']) as m:
        for infile in kwargs['infiles']:
            for data in parse_data(infile):

                query_result = m.query(Project, 'project_id', data['project_id']).first()
                if query_result:
                    print('*** skip ***', query_result)
                    continue
                
                project = Project(**data)

                if not kwargs['no']:
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


if __name__ == '__main__':
    main()
