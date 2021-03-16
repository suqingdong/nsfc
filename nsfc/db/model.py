from sqlalchemy import Column, Integer, Float, DECIMAL, String, DATETIME, ForeignKey, BOOLEAN, Index, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.orm.state import InstanceState
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'

    project_id = Column(String(20), primary_key=True, comment='项目编号')

    title = Column(String(200), comment='项目名称')
    project_type = Column(String(50), comment='项目类型')
    project_type_code = Column(String(20), comment='项目类型代码')

    approval_year = Column(Integer, comment='批准年度')
    person = Column(String(20), comment='负责人', index=True)
    money = Column(Float, comment='项目金额(万)')
    institution = Column(String(50), comment='依托单位')

    start_time = Column(Integer, comment='开始时间(YYYYMM)')
    end_time = Column(Integer, comment='结束时间(YYYYMM)')

    subject = Column(String(30), comment='所属学部')
    subject_class_list = Column(String(100), comment='学科分类分级')
    subject_code_list = Column(String(50), comment='学科代码分级')
    subject_code = Column(String(20), comment='学科代码')

    finished = Column(BOOLEAN, comment='是否结题', default=False)

    keyword = Column(String(100), comment='中文关键词')
    keyword_en = Column(String(100), comment='英文关键词')
    abstract = Column(String(1000), comment='中文摘要')
    abstract_en = Column(String(1000), comment='英文摘要')
    abstract_conc = Column(String(1000), comment='结题摘要')
    result_stat = Column(String(30), comment='研究成果统计')

    __table_args__ = (
        Index('search_by_year', 'approval_year'),
        Index('search_by_title', 'title'),
    )

    @property
    def as_dict(self):
        return {k:v for k,v in self.__dict__.items() if not isinstance(v, InstanceState)}

    def __str__(self):
        return '[{project_id} - {title}]'.format(**self.__dict__)

    __repr__ = __str__


# class FieldCode(Base):
#     __tablename__ = 'field_code'
#     code = Column(String(20), comment='学科代码')
#     name = Column(String(20), comment='学科名称')


# class SupportType(Base):
#     __tablename__ = 'support_type'
#     code = Column(String(20), comment='类别代码')
#     name = Column(String(20), comment='类别名称')


if __name__ == '__main__':
    data = {'approval_year': '2019',
            'institution': '中国人民解放军第四军医大学',
            'money': '20',
            'period': '2020-01 - 2022-12',
            'person': '宗春琳',
            'project_id': '81903249',
            'project_type': '青年科学基金项目',
            'subject': '医学科学部',
            'subject_class': '一级：放射医学，二级：放射医学，三级：放射医学',
            'subject_code': '一级：H22，二级：H2201，三级：H2201',
            'title': '放射性颌骨骨坏死中巨噬细胞外泌体对肌成纤维细胞的调控作用及机制研究'}
    p = Project(**data)
    print(p)