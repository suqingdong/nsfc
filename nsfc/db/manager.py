import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.state import InstanceState

from .model import Base, Project

from simple_loggers import SimpleLogger


class Manager(object):
    """
        uri:
            - sqlite:///relative/path/to/db
            - sqlite:////absolute/path/to/db
            - sqlite:///:memory:
    """
    def __init__(self, uri=None, echo=True, drop=False, logger=None):
        self.uri = uri or 'sqlite:///:memory:'
        self.logger = logger or SimpleLogger('Manager')
        self.engine = sqlalchemy.create_engine(uri, echo=echo)
        self.engine.logger.level = self.logger.level

        self.session = self.connect()
        self.create_table(drop=drop)
    
    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.session.commit()
        self.session.close()
        self.logger.debug('database closed.')

    def connect(self):
        self.logger.debug('connecting to: {}'.format(self.uri))
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        return session

    def create_table(self, drop=False):
        if drop:
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def query(self, Meta, key, value):
        if key not in Meta.__dict__:
            self.logger.warning(f'unavailable key: {key}')
            return None
        res = self.session.query(Meta).filter(Meta.__dict__[key]==value)
        return res

    def insert(self, Meta, key, datas, upsert=True):
        """
            upsert: add when key not exists, update when key exists
        """
        if isinstance(datas, Base):
            datas = [datas]

        for data in datas:
            res = self.query(Meta, key, data.__dict__[key])
            if not res.first():
                self.logger.debug(f'>>> insert data: {data}')
                self.session.add(data)
            elif upsert:
                self.logger.debug(f'>>> update data: {data}')
                context = {k: v for k, v in data.__dict__.items() if not isinstance(v, InstanceState)}
                res.update(context)

    

if __name__ == '__main__':
    # uri = 'sqlite:///:memory:'
    # uri = 'sqlite:///./project.db'
    # uri = 'sqlite:////path/to/test.db'
    # m = Manager(uri)
    # m.create_table()

    uri = 'sqlite:///./project.1997_2000.db'

    with Manager(uri=uri, echo=False) as m:
        # m.create_table()
        res = m.query(Project, 'project_id', '10001001')
        print(dir(res))



    