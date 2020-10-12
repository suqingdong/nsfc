===========
安装说明
===========

Install with ``pip``::

    pip install nsfc


==========
基本用法
==========

查看帮助
==========

.. code:: console

    nsfc

.. image:: https://suqingdong.github.io/nsfc/help/example1.png


查看申请代码/资助类别
=======================

.. code:: console

    nsfc show-codes -t S
    nsfc show-codes -t Z

在线查看：https://suqingdong.github.io/nsfc/help/index.html


资助项目查询
=======================

.. code:: console

    # 1 运行时选择申请代码和批准年度
    - nsfc search

    # 2 指定申请代码和批准年度，多个值之间可用逗号分隔
    - nsfc search -c C05,C06 -y 2018,2019,2020

    # 3 指定查询类型(Z: 资助项目[默认]，J: 结题项目)
    - nsfc search -c C05,C06 -y 2018,2019,2020 -t J

    # 4 指定输出文件和格式(html, xlsx, txt/tsv, json, jl, pkl)
    - nsfc search -c C05 -y 2019 -o out [默认 -O xlsx]
    - nsfc search -c C05 -y 2019 -o out -O html
    - nsfc search -c C05 -y 2019 -o out -O tsv
    - nsfc search -c C05 -y 2019 -o out -O json
    - nsfc search -c C05 -y 2019 -o out -O jl

结果示例
=======================

* html: https://suqingdong.github.io/nsfc/examples/demo.html
* json: https://suqingdong.github.io/nsfc/examples/demo.json
* excel: https://suqingdong.github.io/nsfc/examples/demo.xlsx
