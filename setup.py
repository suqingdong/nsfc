# -*- encoding: utf8 -*-
import os
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from nsfc import __version__, __author__, __author_email__


setup(
    name='nsfc',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description='国家自然科学基金查询',
    long_description=open(os.path.join(BASE_DIR, 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/nsfc',
    project_urls={
        'Documentation': 'https://nsfc.readthedocs.io',
        'Tracker': 'https://github.com/suqingdong/nsfc/issues',
    },
    license='BSD License',
    install_requires=open(os.path.join(BASE_DIR, 'requirements.txt')).read().split('\n'),
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'nsfc = nsfc.bin.__init__:cli',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
