# 国家自然科学基金查询
---
## 查询网站
### http://output.nsfc.gov.cn
> API接口较好，但资助项目检索需要验证码
> - 资助项目检索：http://output.nsfc.gov.cn/fundingQuery
> - 结题项目检索：http://output.nsfc.gov.cn/projectQuery
> - 结题项目详情：http://output.nsfc.gov.cn/conclusionProject/30360042
> - 申请代码：http://output.nsfc.gov.cn/common/data/fieldCode
> - 资助类别：http://output.nsfc.gov.cn/common/data/supportTypeData
> - 资助类别(仅一级分类)：http://output.nsfc.gov.cn/common/data/supportTypeClassOneData

## 安装
```bash
pip install nsfc
```

## 使用示例
#### 查看申请代码/资助类别
```
nsfc show-codes -t S
nsfc show-codes -t Z
```
#### 资助项目查询
```
# 1 运行时选择申请代码和批准年度
nsfc search

# 2 指定申请代码和批准年度，多个值之间可用逗号分隔
nsfc search -c C05,C06 -y 2018,2019,2020

# 3 指定查询类型(Z: 资助项目[默认]，J: 结题项目)
nsfc search -c C05,C06 -y 2018,2019,2020 -t J

# 4 指定输出文件，根据后缀判断格式(html, xlsx, csv/tsv, json, jl, pkl)
nsfc search -c C05 -y 2019 -o out.html
nsfc search -c C05 -y 2019 -o out.xlsx
nsfc search -c C05 -y 2019 -o out.tsv
nsfc search -c C05 -y 2019 -o out.json
```


## 结果示例
