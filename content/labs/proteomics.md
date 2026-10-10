---
title: "实验 17：蛋白质组定量分析"
date: "2026-10-10"
weight: 170
category: "多组学"
meta: "组学 · 约 60 分钟"
module: "multi-omics"
draft: false
summary: "质谱给出的是谱图，要经搜库才变成蛋白与定量值。本实验走完数据获取、搜库、过滤、归一化与差异分析，并重点讲清缺失值为什么不能填 0。"
---

> 所属模块：[多组学整合分析](../posts/multi-omics.html)

## 一、实验目的

<ul>
  <li>了解蛋白质组学的基本流程：酶解 → LC-MS/MS →搜库 → 定量 → 统计；</li>
  <li>会用 MaxQuant / FragPipe 完成一次搜库，理解 FDR 与酶切参数；</li>
  <li>区分 <strong>DDA 与 DIA</strong>、<strong>标记（TMT/iTRAQ）与非标记（LFQ）</strong>定量；</li>
  <li>掌握缺失值处理与差异蛋白筛选的正确做法。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具 / 数据库</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>PRIDE / ProteomeXchange</td><td>公开蛋白组原始数据</td><td><a href="https://www.ebi.ac.uk/pride/" target="_blank" rel="noopener">PRIDE</a></td></tr>
    <tr><td>MaxQuant</td><td>经典搜库与定量流程</td><td><a href="https://www.maxquant.org/" target="_blank" rel="noopener">MaxQuant</a></td></tr>
    <tr><td>FragPipe / MSFragger</td><td>快速搜库，支持 DIA</td><td><a href="https://fragpipe.nesvilab.org/" target="_blank" rel="noopener">FragPipe</a></td></tr>
    <tr><td>Perseus</td><td>下游统计与可视化</td><td><a href="https://www.maxquant.org/perseus/" target="_blank" rel="noopener">Perseus</a></td></tr>
    <tr><td>UniProt</td><td>搜库用的蛋白序列库</td><td><a href="https://www.uniprot.org/" target="_blank" rel="noopener">UniProt</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 获取原始数据**

在 <a href="https://www.ebi.ac.uk/pride/" target="_blank" rel="noopener">PRIDE</a> 检索相关研究，下载 raw（或转换后的 mzML）文件与对应的实验设计（哪个文件属于哪一组）。

**2. 搜库**

MaxQuant 关键设置：

<ul>
  <li><strong>FASTA 数据库</strong>：UniProt 对应物种的参考蛋白组（最好加上常见污染序列库）；</li>
  <li><strong>酶</strong>：胰蛋白酶 Trypsin/P，允许漏切位点（missed cleavages）一般设 2；</li>
  <li><strong>修饰</strong>：固定修饰常用半胱氨酸烷基化（Carbamidomethyl），可变修饰常用甲硫氨酸氧化与 N 端乙酰化；</li>
  <li><strong>FDR</strong>：蛋白与肽段水平均设 <strong>1%</strong>（蛋白水平 FDR 是发表的最低要求）。</li>
</ul>

<p>修饰不要"越多越好"：盲目增加可变修饰会急剧放大搜索空间，反而降低 FDR 控制后的有效鉴定数。</p>

**3. 结果过滤**

```r
# proteinGroups.txt 读入后的常规三步过滤
dat <- dat[dat$Reverse != "+", ]        # 去掉反向诱饵序列
dat <- dat[dat$Potential.contaminant != "+", ]   # 去掉污染蛋白
dat <- dat[dat$Q.value < 0.01 & !is.na(dat$Q.value), ]
```

<ul>
  <li><strong>Reverse（诱饵）</strong>与 <strong>Contaminant（角蛋白、胰蛋白酶等）</strong>必须剔除；</li>
  <li>只用"至少 2 条唯一肽段（unique peptides）"支持的蛋白，可显著提高可靠性。</li>
</ul>

**4. 定量与归一化**

<ul>
  <li><strong>LFQ（非标记）</strong>：用 MaxQuant 的 LFQ intensity，先做 log2 转换，再做中位数归一化或 vsn；</li>
  <li><strong>TMT / iTRAQ（标记）</strong>：用 reporter ion 强度，需做通道间归一化（如 IRS、median normalization）以消除标记效率与上样量差异。</li>
</ul>

**5. 缺失值处理（关键）**

<p>蛋白组数据的缺失值通常<strong>不是随机的</strong>：低丰度蛋白更容易检测不到（MNAR）。直接填 0 会人为制造"某组完全不表达"的假象。常见做法：</p>

<ul>
  <li>先按"至少在某一组中 N 个样本有值"过滤；</li>
  <li>再用左移高斯分布（如 Perseus 的 imputation）或 KNN / MinProb 填补；</li>
  <li>报告中必须说明填补方法与比例。</li>
</ul>

**6. 差异分析**

```r
library(limma)
design <- model.matrix(~ 0 + group)
fit <- lmFit(log2_intensity, design)
fit <- eBayes(contrasts.fit(fit, makeContrasts(treat - ctrl, levels = design)))
topTable(fit, adjust = "BH", number = Inf)
```

## 四、结果判读

<ul>
  <li><strong>先看鉴定数量与 FDR</strong>：一个样本的鉴定蛋白数与文献同类型实验相当才算正常；明显偏少要检查酶、修饰与数据库。</li>
  <li><strong>看强度分布的箱线图</strong>：归一化后各样本中位数应基本对齐，否则样本间不可直接比较。</li>
  <li><strong>差异蛋白阈值</strong>：常用 <code>FDR &lt; 0.05 且 |log2FC| &gt; 1</code>。蛋白组的差异倍数通常比转录组小，阈值需要结合数据调整。</li>
  <li><strong>与转录组的相关性通常不高</strong>：这是正常现象（翻译调控、蛋白降解、检测灵敏度差异），不要因为"mRNA 涨了蛋白没涨"就认为实验失败。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>缺失值填 0</strong>：蛋白组分析中最常见的错误，会严重扭曲统计结果。</li>
  <li><strong>共享肽段导致定量错误</strong>：同一肽段属于多个蛋白时，MaxQuant 会归入 protein group，需要明确报告的是"蛋白组"而非单一蛋白。</li>
  <li><strong>批次效应</strong>：质谱信号随时间漂移，样本上机顺序应随机化，否则批次与分组会混淆。</li>
  <li><strong>修饰设置随意</strong>：过多可变修饰会让 FDR 急剧恶化。</li>
  <li><strong>把 DDA 与 DIA 混为一谈</strong>：DIA 需要谱图库或 library-free 流程（如 DIA-NN），不能照搬 DDA 参数。</li>
</ul>

## 六、练习

<ol>
  <li>在 PRIDE 找一个与你的物种相关的蛋白组数据集，记录编号与样本数。</li>
  <li>列出搜库时必须设置的 5 个参数及你选择的理由。</li>
  <li>对一份 proteinGroups.txt 做三步过滤，报告过滤前后蛋白数。</li>
  <li>画归一化前后的箱线图，说明是否需要归一化。</li>
  <li>（选做）用 limma 做两组差异分析，比较"填 0"与"高斯填补"两种处理下差异蛋白数的差别。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://www.maxquant.org/maxquant/documentation" target="_blank" rel="noopener">MaxQuant 文档</a></li>
  <li><a href="https://fragpipe.nesvilab.org/docs/tutorial_fragpipe.html" target="_blank" rel="noopener">FragPipe 教程</a></li>
  <li><a href="https://www.ebi.ac.uk/pride/" target="_blank" rel="noopener">PRIDE 数据库</a></li>
  <li><a href="https://www.uniprot.org/help/proteomes" target="_blank" rel="noopener">UniProt 蛋白组下载</a></li>
</ul>
