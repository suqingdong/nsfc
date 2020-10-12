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

## 依赖
- Linux/Windows
- Python2/Python3
- tesseract

### `tesseract` 是图像识别工具，用于识别验证码
#### Linux
```
yum install tesseract
```

#### Windows
- [官网](https://digi.bib.uni-mannheim.de/tesseract/)
- [百度云](https://pan.baidu.com/s/1k7u01BE8e2zu5AoubE5FOw)(提取码: `5nxb`)
> 安装后需要把tesseract添加到环境变量中
![](https://suqingdong.github.io/nsfc/help/windows_path_add.png)
![](https://suqingdong.github.io/nsfc/help/tesseract.png)

## 安装
```bash
pip install nsfc
```

## 使用示例
#### 查看帮助
```
nsfc
```

#### 查看申请代码/资助类别
```
nsfc show-codes -t S
nsfc show-codes -t Z
```
> 在线查看：https://suqingdong.github.io/nsfc/help/index.html

#### 资助项目查询
```
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
```

## 结果示例
- [html](https://suqingdong.github.io/nsfc/examples/demo.html)
- [json](https://suqingdong.github.io/nsfc/examples/demo.json)
- [excel](https://suqingdong.github.io/nsfc/examples/demo.xlsx)
