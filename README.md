[![Downloads](https://pepy.tech/badge/nsfc)](https://pepy.tech/project/nsfc)
![GitHub last commit](https://img.shields.io/github/last-commit/suqingdong/nsfc)
![GitHub Repo stars](https://img.shields.io/github/stars/suqingdong/nsfc?style=social)

# 国家自然科学基金数据查询系统

## 安装
```bash
pip3 install nsfc
```

## 数据下载
> 数据库文件较大，可通过百度网盘进行下载
> ([下载链接](https://pan.baidu.com/s/1eadrfUg1ovBF1EAXWSTV-w) 提取码: `2nw5`)
- 下载所需的数据库文件，如project.A.sqlite3, 或全部数据project.all.sqlite3
- 保存至`nsfc`的安装路径下的`data`目录下, 如：`/path/to/site-packages/nsfc/data/project.db`
- 或者保存至`HOME`路径下的`nsfc_data`目录下，如`~/nsfc_data/project.db`
- 也可以通过`-d`参数指定要使用的数据库文件

## 使用示例
### 本地查询
```bash
# 查看帮助
nsfc query
```
![](https://suqingdong.github.io/nsfc/examples/query-help.png)

```bash
# 列出可用的查询字段
nsfc query -K
```
![](https://suqingdong.github.io/nsfc/examples/query-keys.png)

```bash
# 输出数量
nsfc query -C
```
![](https://suqingdong.github.io/nsfc/examples/query-count.png)

```bash
# 按批准年份查询
nsfc query -C -s approval_year 2019
```
![](https://suqingdong.github.io/nsfc/examples/query-count-year.png)

```bash
# 按批准年份+学科代码(模糊)
nsfc query -C -s approval_year 2019 -s subject_code "%A%"
```
![](https://suqingdong.github.io/nsfc/examples/query-year-and-subject.png)

```bash
# 批准年份也可以是一个区间
nsfc query -C -s approval_year 2015-2019 -s subject_code "%C01%"
```
![](https://suqingdong.github.io/nsfc/examples/query-year-region.png)

```bash
# 结果输出为.jl文件
nsfc query -s approval_year 2019 -s subject_code "%C0501%" -o C0501.2019.jl
```
![](https://suqingdong.github.io/nsfc/examples/query-output-jl.png)

```bash
# 结果输出为xlsx文件
nsfc query -s approval_year 2019 -s subject_code "%C0501%" -o C0501.2019.xlsx -F xlsx
```
![](https://suqingdong.github.io/nsfc/examples/query-output-xlsx.png)

```bash
# 限制最大输出条数
nsfc query -L 5 -s approval_year 2019                                           
```

#### 结题报告下载
```bash
nsfc report 20671004

nsfc report 20671004 -o out.pdf
```

### 其他功能
#### LetPub数据获取
```bash
nsfc crawl
```

#### 本地数据库构建/更新
```bash
nsfc build
```

#### 其他说明
- 目前基本上只有2019年之前的数据，2020年的数据很少
- 后续有数据时会再更新
