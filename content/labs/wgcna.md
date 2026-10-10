---
title: "实验 12：加权基因共表达网络分析（WGCNA）"
date: "2026-10-10"
weight: 120
category: "多组学"
meta: "组学 · 约 60 分钟"
module: "multi-omics"
draft: false
summary: "差异表达看的是单个基因，WGCNA 看的是成组的基因模块。本实验用 R 包 WGCNA 建网、识别模块、关联性状并挑出枢纽基因。"
---

> 所属模块：[多组学整合分析](../posts/multi-omics.html)

## 一、实验目的

<ul>
  <li>理解共表达网络的基本单元：模块（module）、特征基因（eigengene）、连接度（connectivity）；</li>
  <li>会用 WGCNA 完成软阈值选择、模块识别与模块合并；</li>
  <li>能把模块与表型性状关联，找出<strong>枢纽基因</strong>；</li>
  <li>知道样本量与离群样本对结果的影响。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>WGCNA（R 包）</td><td>建网与模块识别</td><td><a href="https://horvath.genetics.ucla.edu/html/CoexpressionNetwork/Rpackages/WGCNA/" target="_blank" rel="noopener">官方教程</a></td></tr>
    <tr><td>Cytoscape</td><td>网络可视化</td><td><a href="https://cytoscape.org/" target="_blank" rel="noopener">cytoscape.org</a></td></tr>
    <tr><td>clusterProfiler</td><td>模块功能注释</td><td><a href="https://bioconductor.org/packages/clusterProfiler/" target="_blank" rel="noopener">clusterProfiler</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 准备表达矩阵**

<p>建议<strong>不少于 15–20 个样本</strong>（样本越少网络越不稳定），并预先过滤低表达基因：</p>

```r
library(WGCNA)
dat <- read.delim("expr_matrix.tsv", row.names = 1)
dat <- dat[rowSums(dat > 1) >= 3, ]        # 去掉几乎不表达的基因
```

**2. 检查离群样本**

```r
sampleTree <- hclust(dist(t(dat)), method = "average")
plot(sampleTree)                            # 明显离群的分支应剔除
```

**3. 选软阈值（soft threshold）**

```r
powers <- c(1:20)
sft <- pickSoftThreshold(dat, powerVector = powers, verbose = 5)
plot(sft$fitIndices[,1], -sign(sft$fitIndices[,3]) * sft$fitIndices[,2],
     xlab = "Soft Threshold (power)", ylab = "Scale Free Topology Model Fit")
```

选<strong>无标度拓扑拟合指数达到 0.8 左右的最小 power</strong>（常用 6–12）。

**4. 构建网络与识别模块**

```r
net <- blockwiseModules(dat, power = sft$powerEstimate,
                        TOMType = "unsigned", minModuleSize = 30,
                        reassignThreshold = 0, mergeCutHeight = 0.25,
                        numericLabels = TRUE, verbose = 3)
table(net$colors)                           # 各模块基因数
MEs <- net$MEs
```

**5. 模块与性状关联**

```r
trait <- read.delim("traits.tsv", row.names = 1)
modTrait <- cor(MEs, trait, use = "p")
modTraitP <- corPvalueStudent(modTrait, nrow(dat))
heatmap <- labeledHeatmap(Matrix = modTrait, xLabels = colnames(trait),
                          yLabels = names(MEs), colorLabels = FALSE)
```

**6. 找枢纽基因（hub gene）**

```r
# 模块内连接度
ADJ <- adjacency(dat, power = sft$powerEstimate)
k <- intramodularConnectivity(ADJ, net$colors)
hub <- rownames(k)[order(-k$kWithin, )[1:20]]     # 取连接度最高的 20 个
```

**7. 导出到 Cytoscape**

```r
TOM <- TOMsimilarityFromExpr(dat, power = sft$powerEstimate)
cyt <- exportNetworkToCytoscape(TOM, edgeFile = "edges.txt",
                                nodeFile = "nodes.txt", threshold = 0.15)
```

## 四、结果判读

<ul>
  <li><strong>软阈值曲线</strong>：拟合指数随 power 上升后趋平。取刚达到 0.8 的那个值；若怎么都达不到，说明数据不适合做无标度网络（样本异质性太大或基因过滤不当）。</li>
  <li><strong>模块数量</strong>：<code>table(net$colors)</code> 里灰色（grey）模块是"未归入任何模块"的基因集合，比例过高说明网络构建不理想。</li>
  <li><strong>模块-性状相关系数</strong>：看 <code>cor</code> 值与显著性 p。绝对值大且 p 小的模块才值得追；相关不等于因果，模块与性状之间是<strong>统计关联</strong>。</li>
  <li><strong>枢纽基因</strong>：模块内连接度最高的基因，常是调控核心，但它是<strong>候选</strong>，需实验或独立数据验证。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>样本量太少</strong>：少于 15 个样本的结果很难重复。这是 WGCNA 最常被审稿人质疑的地方。</li>
  <li><strong>不做离群样本检查</strong>：一个异常样本会扭曲整个相关矩阵。</li>
  <li><strong>批次效应未去除</strong>：模块可能反映批次而非生物学，先做 PCA 检查。</li>
  <li><strong>参数照抄</strong>：<code>power</code>、<code>minModuleSize</code>、<code>mergeCutHeight</code> 都要按数据调整，换数据集不能不动参数。</li>
  <li><strong>把模块直接当通路</strong>：模块是共表达簇，需再做富集才知道可能参与什么过程。</li>
</ul>

## 六、练习

<ol>
  <li>用一份 ≥15 样本的表达矩阵跑样本聚类，判断是否需要剔除离群样本。</li>
  <li>运行 <code>pickSoftThreshold</code>，记录你选择的 power 与对应的拟合指数。</li>
  <li>建网后统计模块数与 grey 模块基因占比。</li>
  <li>做一个性状关联热图，指出相关性最强且显著的模块。</li>
  <li>（选做）对该模块基因做 GO 富集，并导出前 20 个枢纽基因。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://horvath.genetics.ucla.edu/html/CoexpressionNetwork/Rpackages/WGCNA/Tutorials/" target="_blank" rel="noopener">WGCNA 官方教程合集</a></li>
  <li><a href="https://cytoscape.org/documentation_users.html" target="_blank" rel="noopener">Cytoscape 文档</a></li>
</ul>
