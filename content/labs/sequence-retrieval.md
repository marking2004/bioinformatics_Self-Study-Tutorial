---
title: "实验 5：序列获取与原始数据下载"
date: "2026-10-10"
weight: 50
category: "数据库"
meta: "资源 · 约 45 分钟"
module: "databases"
draft: false
summary: "同一个数据可以从网页点、也可以从命令行拉。本实验两种方式都练：E-utilities 批量取序列、SRA Toolkit 取原始测序数据、ENA/DDBJ 换源下载，并校验完整性。"
---

> 所属模块：[常用生物信息数据库简介](../posts/databases.html)

## 一、实验目的

<ul>
  <li>掌握网页与命令行两条取数路径，知道什么时候该用哪条；</li>
  <li>用 <strong>Entrez Direct（E-utilities）</strong>按条件批量取序列；</li>
  <li>用 <strong>SRA Toolkit</strong> 下载原始测序数据；</li>
  <li>学会校验下载结果（条数、行数、md5），避免"跑完流程才发现数据少了一半"。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具 / 接口</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>Entrez Direct</td><td>NCBI 命令行检索与取数</td><td><a href="https://www.ncbi.nlm.nih.gov/books/NBK179288/" target="_blank" rel="noopener">官方手册</a></td></tr>
    <tr><td>SRA Toolkit</td><td>原始测序数据下载与转换</td><td><a href="https://github.com/ncbi/sra-tools" target="_blank" rel="noopener">GitHub</a></td></tr>
    <tr><td>ENA Browser API</td><td>EBI 侧序列与数据下载</td><td><a href="https://www.ebi.ac.uk/ena/browser/api/" target="_blank" rel="noopener">API 文档</a></td></tr>
    <tr><td>DDBJ</td><td>日本侧同源入口</td><td><a href="https://www.ddbj.nig.ac.jp/" target="_blank" rel="noopener">DDBJ</a></td></tr>
    <tr><td>Ensembl REST / BioMart</td><td>基因组批量取序</td><td><a href="https://rest.ensembl.org/" target="_blank" rel="noopener">REST</a> · <a href="https://www.ensembl.org/biomart/martview" target="_blank" rel="noopener">BioMart</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 网页方式：单条与少量**

NCBI 记录页 → <em>Send to</em> → <em>File</em> → 选格式保存。几条序列用网页最省事；超过几十条就该换命令行。

**2. 命令行方式：E-utilities**

```bash
# 检索：水稻 NHX 基因的核酸记录
esearch -db nuccore -query "Oryza sativa[Organism] AND NHX[Gene Name]" > esearch.xml
# 取序列
efetch -db nuccore -format fasta -input esearch.xml > nhx.fasta
# 一步到位（管道）
esearch -db nuccore -query "Oryza sativa[Organism] AND NHX[Gene Name]" \
  | efetch -format fasta > nhx.fasta

grep -c ">" nhx.fasta     # 看看拿到几条
```

常用参数：<code>-db</code>（nuccore / protein / sra / pubmed）、<code>-format</code>（fasta / genbank / gb）、<code>-id</code>（直接给 accession 列表）。

**3. 下载原始测序数据（SRA）**

```bash
prefetch SRR12345678                              # 下载 .sra 包
fasterq-dump SRR12345678 --split-files --gzip     # 转 FASTQ，双端自动拆 R1/R2
```

ENA 侧同样的数据可以直接取 FASTQ，常常更快：

```bash
curl -L "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRR12345678&result=read_run&fields=fastq_ftp" 
# 返回的 FTP 地址拼上 http 前缀即可 wget / curl 下载
```

**4. 从 Ensembl 取基因组区段**

```bash
curl "https://rest.ensembl.org/sequence/region/human/1:1000000-1000500:1?content-type=text/plain"
```

批量取基因列表用 BioMart 网页勾选属性后导出，比写 API 省时间。

**5. 校验下载结果**

```bash
seqkit stats nhx.fasta                 # 序列条数与长度
wc -l reads.fastq                      # FASTQ 行数应为 reads 数 × 4
md5sum reads.fastq.gz                  # 与数据源提供的 md5 比对
```

## 四、结果判读

<ul>
  <li><strong>FASTQ 行数 = reads 数 × 4</strong>（每条 read 占 4 行）。除不尽说明文件被截断或拼接错误，必须重新下载。</li>
  <li><strong>双端数据必须成对</strong>：R1 与 R2 的 reads 数完全相同，且 ID 顺序一致。不等就不能直接进比对流程。</li>
  <li><code>esearch</code> 返回的 <code>Count</code> 与 <code>efetch</code> 实际拿到的条数应一致；差很多通常是中间有临时记录或权限限制。</li>
  <li>下载中断会产生"看起来存在但不完整"的文件——<strong>校验通过才算拿到数据</strong>。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>NCBI 限速</strong>：无 API key 时每秒最多约 3 次请求。批量取数要么加 API key、要么在循环里加 <code>sleep</code>，否则会被临时封 IP。</li>
  <li><strong>磁盘空间</strong>：一个样本的 SRA 常有几 GB，<code>fasterq-dump</code> 解压后更大。先 <code>df -h</code>。</li>
  <li><strong>SRA Toolkit 版本</strong>：旧版不支持某些新格式，报错时先升级（推荐 conda 安装）。</li>
  <li><strong>网络中断</strong>：大文件用 <code>wget -c</code>（断点续传）或 <code>aria2c</code>，别用浏览器下载框。</li>
  <li><strong>物种基因组版本</strong>：Ensembl 与 NCBI 的基因组版本号不同，混用会导致坐标对不上。</li>
</ul>

## 六、练习

<ol>
  <li>用 <code>esearch</code> 检索你熟悉的物种某个基因家族，记录命中条数与检索式。</li>
  <li>把结果导出为 FASTA，用 <code>seqkit stats</code> 报告条数、最短与最长长度。</li>
  <li>下载一个公开的 SRA 单端数据集，验证 FASTQ 行数能被 4 整除。</li>
  <li>用 ENA 的 API 查询同一 accession，比较两种来源的下载速度。</li>
  <li>（选做）写一个 shell 循环，从 accession 列表文件批量下载并自动校验。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://www.ncbi.nlm.nih.gov/books/NBK179288/" target="_blank" rel="noopener">Entrez Direct 官方手册</a></li>
  <li><a href="https://github.com/ncbi/sra-tools/wiki/HowTo:-fasterq-dump" target="_blank" rel="noopener">fasterq-dump 用法</a></li>
  <li><a href="https://www.ebi.ac.uk/ena/browser/api/" target="_blank" rel="noopener">ENA Browser API</a></li>
  <li><a href="https://rest.ensembl.org/documentation" target="_blank" rel="noopener">Ensembl REST 文档</a></li>
</ul>
