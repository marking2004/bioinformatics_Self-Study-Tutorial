---
title: "实验 3：Python 基础与序列提取"
date: "2026-10-10"
weight: 30
category: "编程基础"
meta: "基础 · 约 45 分钟"
module: "programming"
draft: false
summary: "序列本质是文本，Python 处理它最顺手。本实验用 Biopython 读写 FASTA/GenBank，按 ID 抽序列、算 GC 含量、做反向互补，并批量输出。"
---

> 所属模块：[编程基础：R 与 Python](../posts/programming.html)

## 一、实验目的

<ul>
  <li>掌握 Python 的字符串、列表、字典与文件读写；</li>
  <li>用 <strong>Biopython</strong> 解析 FASTA 与 GenBank 文件；</li>
  <li>实现三个高频动作：按 ID 抽序列、统计 GC 含量、反向互补；</li>
  <li>把一次性的操作写成可重跑的脚本。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>Python 3</td><td>语言本体</td><td><a href="https://www.python.org/" target="_blank" rel="noopener">python.org</a></td></tr>
    <tr><td>Biopython</td><td>序列文件解析</td><td><a href="https://biopython.org/" target="_blank" rel="noopener">biopython.org</a></td></tr>
    <tr><td>conda / mamba</td><td>环境与依赖</td><td><a href="https://docs.conda.io/projects/miniconda/en/latest/" target="_blank" rel="noopener">Miniconda</a></td></tr>
    <tr><td>Jupyter</td><td>交互式调试</td><td><a href="https://jupyter.org/" target="_blank" rel="noopener">jupyter.org</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 建环境**

```bash
conda create -n pybio python=3.11 -y
conda activate pybio
conda install -c conda-forge biopython jupyter -y
```

**2. 三个必须熟练的结构**

```python
name = "AtNHX1"                      # 字符串
seqs = ["ATGCGT", "TTACGA"]          # 列表
d = {"AtNHX1": "ATGCGT", "AtSOS1": "TTACGA"}   # 字典：ID -> 序列
print(d[name])
for k, v in d.items():               # 遍历
    print(k, len(v))
```

**3. 读写文本**

```python
with open("ids.txt") as fh:
    ids = [line.strip() for line in fh if line.strip()]
with open("out.txt", "w") as fh:
    fh.write("\n".join(ids))
```

**4. 读 FASTA**

```python
from Bio import SeqIO

for rec in SeqIO.parse("seqs.fasta", "fasta"):
    print(rec.id, len(rec.seq), rec.description)
```

**5. 按 ID 抽取序列**

```python
wanted = {"AtNHX1", "AtHKT1"}
kept = [r for r in SeqIO.parse("seqs.fasta", "fasta") if r.id in wanted]
SeqIO.write(kept, "subset.fasta", "fasta")
```

**6. GC 含量与反向互补**

```python
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

s = Seq("ATGCGTACGGATC")
print(f"GC: {gc_fraction(s):.2%}")
print("反向互补:", s.reverse_complement())
print("翻译:", s.translate())
```

**7. 解析 GenBank，取出 CDS**

```python
for rec in SeqIO.parse("record.gb", "genbank"):
    print(rec.id, rec.annotations.get("organism"))
    for feat in rec.features:
        if feat.type == "CDS":
            prod = feat.qualifiers.get("product", ["-"])[0]
            print("  CDS:", prod, feat.location)
```

**8. 整理成脚本**

```python
#!/usr/bin/env python3
"""subset_fasta.py 按给定的 ID 列表抽取序列"""
import sys
from Bio import SeqIO

ids = {l.strip() for l in open(sys.argv[1]) if l.strip()}
kept = [r for r in SeqIO.parse(sys.argv[2], "fasta") if r.id in ids]
SeqIO.write(kept, sys.argv[3], "fasta")
print(f"kept {len(kept)} / wanted {len(ids)}")
```

## 四、结果判读

<ul>
  <li>脚本最后打印的 <strong>kept 与 wanted 数量应当一致</strong>；若 kept 更少，说明有 ID 没匹配上——多半是 ID 带了版本号（<code>.1</code>）或空格后的描述被算进了 ID。</li>
  <li>GC 含量异常（如 &gt;80% 或 &lt;20%）通常提示序列有问题：污染、接头未去、或物种本身极端，需要回头查原始数据。</li>
  <li>GenBank 的 CDS feature 会带 <code>join(...)</code> 位置（真核基因有内含子），直接切序列会出错，要用 <code>feat.extract(rec.seq)</code>。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>ID 与描述混淆</strong>：<code>rec.id</code> 取 <code>&gt;</code> 后第一个空格前的内容，<code>rec.description</code> 是整行。比对 ID 用 <code>rec.id</code>。</li>
  <li><strong>编码</strong>：打开别人给的文件报 <code>UnicodeDecodeError</code> 时，加 <code>encoding="utf-8"</code> 或用 <code>errors="ignore"</code> 应急。</li>
  <li><strong>换行符</strong>：Windows 生成的 FASTA 在 Linux 上解析可能多出 <code>\r</code>，导致序列末尾异常。</li>
  <li><strong>环境混乱</strong>：不同项目用不同 conda 环境，别把所有包都装进 base。</li>
</ul>

## 六、练习

<ol>
  <li>写一个含 5 条序列的 FASTA，用脚本统计每条的长度与 GC 含量。</li>
  <li>给定 3 个 ID，从上述文件中抽出对应序列，写成新文件。</li>
  <li>对其中一条序列做反向互补并翻译，检查是否有终止符 <code>*</code>。</li>
  <li>下载一个真实 GenBank 记录（见<a href="sequence-databases.html">实验 4</a>），用 Python 打印其 organism 与全部 CDS 产物名。</li>
  <li>（选做）把第 1 题改成一次处理目录下所有 FASTA 文件。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://biopython.org/wiki/Documentation" target="_blank" rel="noopener">Biopython 官方文档</a></li>
  <li><a href="https://biopython.org/docs/1.81/api/Bio.SeqIO.html" target="_blank" rel="noopener">SeqIO API</a></li>
  <li><a href="https://rosalind.info/problems/locations/" target="_blank" rel="noopener">Rosalind 编程练习</a></li>
</ul>
