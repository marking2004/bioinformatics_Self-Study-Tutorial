---
title: "编程基础：R 与 Python"
date: "2026-10-10"
weight: 15
category: "编程基础"
meta: "基础 · 约 15 分钟"
draft: false
summary: "生信分析真正跑起来靠的是脚本。R 擅长统计与出图，Python 擅长文本处理与流程粘合。这一模块讲清先学哪个、各自掌握到什么程度算够用。"
---

<p>网页工具能点得动一两个样本，点不动几十上百个；能复现别人的图，改不动别人的流程。到某个节点你一定会需要脚本——本模块就是帮你判断该先学哪一门、学到哪里可以停。</p>

## 1. 为什么绕不开编程

<ul>
  <li><strong>批量</strong>：30 个样本的质控、100 个基因的可视化，脚本一次跑完，手点要点一下午。</li>
  <li><strong>可复现</strong>：脚本是实验记录。三个月后被问"这个数怎么来的"，能直接翻出来重跑。</li>
  <li><strong>可改</strong>：现成流程永远差一点点，会改别人的代码比会跑现成流程值钱得多。</li>
</ul>

## 2. R：统计与出图的主力

<p>生信里 R 的位置非常明确——<strong>差异表达、富集分析、统计检验、出版级图形</strong>几乎都在 R 生态里，尤其 Bioconductor 是转录组下游的事实标准。</p>

<table>
  <thead><tr><th>要掌握</th><th>内容</th><th>说明</th></tr></thead>
  <tbody>
    <tr><td>数据结构</td><td>向量、数据框、因子、缺失值</td><td>数据框（data.frame）是日常主力</td></tr>
    <tr><td>包管理</td><td>CRAN、Bioconductor</td><td>生信包基本来自 Bioconductor，安装方式与 CRAN 不同</td></tr>
    <tr><td>绘图</td><td>ggplot2 语法（数据 + 映射 + 图层）</td><td>学会"图层思维"，比背函数有用</td></tr>
    <tr><td>下游分析</td><td>DESeq2 / edgeR、clusterProfiler</td><td>对应本站 RNA-seq 模块</td></tr>
    <tr><td>环境</td><td>RStudio（现 Posit）</td><td>写脚本 + 看变量 + 出图，一个界面搞定</td></tr>
  </tbody>
</table>

## 3. Python：文本处理与流程粘合

<p>序列本质是文本。<strong>批量改序列名、按 ID 抽序列、解析 GenBank 注释、把几个工具串成流程</strong>，这些 Python 写起来最顺手。</p>

<table>
  <thead><tr><th>要掌握</th><th>内容</th><th>说明</th></tr></thead>
  <tbody>
    <tr><td>基础语法</td><td>字符串、列表、字典、文件读写</td><td>字典是处理"ID → 序列"的核心</td></tr>
    <tr><td>Biopython</td><td>SeqIO 读写 FASTA / GenBank</td><td>生信 Python 的事实标准库</td></tr>
    <tr><td>数据</td><td>pandas、numpy</td><td>表格与矩阵运算</td></tr>
    <tr><td>环境</td><td>conda / mamba、Jupyter</td><td>生信工具多用 conda 装，顺手解决依赖地狱</td></tr>
  </tbody>
</table>

## 4. 先学哪个

<table>
  <thead><tr><th>你的目标</th><th>建议</th></tr></thead>
  <tbody>
    <tr><td>做差异表达、富集、画热图火山图</td><td>先 R，够用很久</td></tr>
    <tr><td>处理序列文件、搭分析流程、爬数据</td><td>先 Python</td></tr>
    <tr><td>时间只够学一门</td><td>R——本科阶段的下游分析大多在 R 里</td></tr>
    <tr><td>打算读研做生信</td><td>两门都要，Python 打底 + R 做统计</td></tr>
  </tbody>
</table>

## 5. 学到什么程度算"够用"

<ul>
  <li>能读懂别人的脚本并改参数；</li>
  <li>能把一个重复动作写成循环；</li>
  <li>报错时能看懂提示、会搜索、会最小复现；</li>
  <li>能把自己的分析整理成一个可重跑的脚本。</li>
</ul>

<p>不需要会写包、不需要懂面向对象、不需要刷算法题。<strong>够用即可，剩下的边做边查。</strong></p>

## 官方资源

<ul>
  <li><a href="https://www.r-project.org/" target="_blank" rel="noopener">R Project</a> · <a href="https://cran.r-project.org/" target="_blank" rel="noopener">CRAN</a> · <a href="https://www.bioconductor.org/" target="_blank" rel="noopener">Bioconductor</a></li>
  <li><a href="https://posit.co/" target="_blank" rel="noopener">Posit（原 RStudio）</a> · <a href="https://ggplot2.tidyverse.org/" target="_blank" rel="noopener">ggplot2</a></li>
  <li><a href="https://www.python.org/" target="_blank" rel="noopener">Python</a> · <a href="https://biopython.org/" target="_blank" rel="noopener">Biopython</a></li>
  <li><a href="https://conda-forge.org/" target="_blank" rel="noopener">conda-forge</a> · <a href="https://bioconda.github.io/" target="_blank" rel="noopener">Bioconda</a> · <a href="https://jupyter.org/" target="_blank" rel="noopener">Jupyter</a></li>
</ul>
