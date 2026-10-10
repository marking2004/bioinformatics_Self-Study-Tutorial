---
title: "实验 2：R 语言基础与数据可视化"
date: "2026-10-10"
weight: 20
category: "编程基础"
meta: "基础 · 约 45 分钟"
module: "programming"
draft: false
summary: "R 是生信下游分析的主力。本实验练会数据结构、文件读写、CRAN 与 Bioconductor 装包，并用 ggplot2 画出第一张像样的图。"
---

> 所属模块：[编程基础：R 与 Python](../posts/programming.html)

## 一、实验目的

<ul>
  <li>熟悉 R 的基本数据结构：向量、数据框、因子；</li>
  <li>能读写 CSV/TSV，能对数据做筛选、汇总与简单统计检验；</li>
  <li>区分并会用<strong>CRAN 与 Bioconductor</strong>两条装包渠道；</li>
  <li>用 ggplot2 画出散点图、柱状图与箱线图。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>R</td><td>语言本体</td><td><a href="https://www.r-project.org/" target="_blank" rel="noopener">r-project.org</a></td></tr>
    <tr><td>RStudio / Posit</td><td>集成环境</td><td><a href="https://posit.co/download/rstudio-desktop/" target="_blank" rel="noopener">下载页</a></td></tr>
    <tr><td>CRAN</td><td>通用包仓库</td><td><a href="https://cran.r-project.org/" target="_blank" rel="noopener">cran.r-project.org</a></td></tr>
    <tr><td>Bioconductor</td><td>生信包仓库</td><td><a href="https://www.bioconductor.org/" target="_blank" rel="noopener">bioconductor.org</a></td></tr>
    <tr><td>ggplot2</td><td>绘图</td><td><a href="https://ggplot2.tidyverse.org/" target="_blank" rel="noopener">ggplot2.tidyverse.org</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 安装与第一个会话**

```r
R.version.string        # 查看版本
getwd()                 # 当前工作目录
setwd("~/lab02")        # 设定工作目录
```

**2. 数据结构**

```r
x <- c(1, 3, 5, 7, 9)          # 向量
x * 2                          # 向量化运算，无需循环
df <- data.frame(
  gene = c("AtNHX1", "AtSOS1", "AtHKT1"),
  tpm  = c(45.2, 12.8, 88.6),
  tissue = c("root", "leaf", "root")
)
df$gene                        # 取列
df[df$tpm > 20, ]              # 按条件筛选行
str(df)                        # 看结构
summary(df$tpm)                # 汇总统计
```

> 注意 `tissue` 被自动转成因子（factor）。做分组统计时它是必需的，做字符串处理时要先 `as.character()`。

**3. 读写文件**

```r
dat <- read.csv("counts.csv", row.names = 1)         # 逗号分隔
dat <- read.delim("counts.tsv", row.names = 1)       # 制表符分隔
write.csv(df, "result.csv", row.names = FALSE)
```

**4. 装包：两条渠道不要混**

```r
install.packages("ggplot2")                          # CRAN
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("DESeq2")                       # Bioconductor
library(ggplot2)
```

> Bioconductor 的版本与 R 版本绑定，升级 R 之前先查它的<a href="https://www.bioconductor.org/about/release-announcements/" target="_blank" rel="noopener">发布公告</a>，否则旧包装不上。

**5. 画图**

```r
p <- ggplot(df, aes(x = tissue, y = tpm, fill = tissue)) +
  geom_boxplot() +
  geom_point(position = position_jitter(width = .15), size = 2) +
  labs(title = "Gene expression by tissue", x = "Tissue", y = "TPM") +
  theme_bw()
ggsave("boxplot.png", p, width = 5, height = 4, dpi = 300)
```

**6. 一个统计检验**

```r
t.test(tpm ~ tissue, data = df)
```

## 四、结果判读

<ul>
  <li><code>str()</code> 输出里 <code>num</code> 是数值、<code>chr</code> 是字符、<code>Factor w/ 2 levels</code> 是因子。类型不对是新手报错的第一大来源。</li>
  <li><code>summary()</code> 给出最小值、四分位数、中位数、均值、最大值——先看它，能立刻发现异常值或全为 0 的列。</li>
  <li><code>t.test</code> 的 <code>p-value</code> 小于 0.05 只说明两组均值差异不太像随机波动，<strong>不等于生物学意义显著</strong>，还要看差异倍数。</li>
  <li><code>ggsave</code> 出图前先在 Plots 窗看一眼；空白图多半是数据为空或 aes 映射写错。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>装包装到一半失败</strong>：多半是编译依赖缺失。Linux 先装 <code>libxml2-dev</code> 等系统库；最省事的办法是用 conda 装 R 及常用包。</li>
  <li><strong>中文乱码</strong>：Windows 下读入 UTF-8 文件可能乱码，用 <code>read.csv(..., fileEncoding = "UTF-8")</code>，或统一把环境设为 UTF-8。</li>
  <li><strong>路径分隔符</strong>：Windows 的 <code>\</code> 在 R 字符串里是转义符，要写成 <code>/</code> 或 <code>\\</code>。</li>
  <li><strong>覆盖原数据</strong>：筛选后直接赋回同名变量，容易把原始数据弄丢。保留一份 <code>raw</code> 是好习惯。</li>
</ul>

## 六、练习

<ol>
  <li>建一个含 6 个基因、3 个样本的表达矩阵数据框，计算每个基因的均值。</li>
  <li>把矩阵写出成 TSV，再读回来，确认行名列都没有错位。</li>
  <li>用 <code>BiocManager::install()</code> 装 <code>clusterProfiler</code>，记录耗时与是否报错。</li>
  <li>画一张散点图，横轴为样本 A、纵轴为样本 B，加一条 <code>y = x</code> 参考线。</li>
  <li>（选做）对两个分组做 t 检验，写出原假设、p 值与结论各一句。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://r4ds.hadley.nz/" target="_blank" rel="noopener">R for Data Science（在线版）</a></li>
  <li><a href="https://posit.co/resources/cheatsheets/" target="_blank" rel="noopener">RStudio 官方速查表</a></li>
  <li><a href="https://www.bioconductor.org/packages/release/BiocViews.html" target="_blank" rel="noopener">Bioconductor 包索引</a></li>
</ul>
