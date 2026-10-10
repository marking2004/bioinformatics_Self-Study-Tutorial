---
title: "实验 14：单细胞转录组分析"
date: "2026-10-10"
weight: 140
category: "多组学"
meta: "组学 · 约 70 分钟"
module: "multi-omics"
draft: false
summary: "单细胞把'组织平均'拆成'每个细胞'。本实验用 Seurat 走完质控、降维聚类、marker 筛选与细胞类型注释，并说明双细胞、批次效应和分辨率这些决定成败的细节。"
---

> 所属模块：[多组学整合分析](../posts/multi-omics.html)

## 一、实验目的

<ul>
  <li>理解单细胞表达矩阵的特点（极度稀疏、barcode/UMI 计数）；</li>
  <li>用 <strong>Seurat</strong> 完成 QC、归一化、降维聚类与 marker 筛选；</li>
  <li>能用已知 marker 或自动注释工具给细胞群定名；</li>
  <li>知道双细胞、批次效应与聚类分辨率如何影响结论。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>Seurat（R）</td><td>主流单细胞分析框架</td><td><a href="https://satijalab.org/seurat/" target="_blank" rel="noopener">satijalab.org</a></td></tr>
    <tr><td>Scanpy（Python）</td><td>Python 侧等价方案</td><td><a href="https://scanpy.readthedocs.io/" target="_blank" rel="noopener">scanpy</a></td></tr>
    <tr><td>Cell Ranger（10x）</td><td>原始数据定量</td><td><a href="https://www.10xgenomics.com/support/software/cell-ranger" target="_blank" rel="noopener">10x Genomics</a></td></tr>
    <tr><td>SingleR / CellMarker</td><td>细胞类型注释</td><td><a href="https://bioconductor.org/packages/SingleR/" target="_blank" rel="noopener">SingleR</a> · <a href="http://117.50.127.228/CellMarker/" target="_blank" rel="noopener">CellMarker</a></td></tr>
    <tr><td>Harmony</td><td>批次校正</td><td><a href="https://github.com/immunogenomics/harmony" target="_blank" rel="noopener">Harmony</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 读入数据**

```r
library(Seurat)
counts <- Read10X(data.dir = "filtered_feature_bc_matrix/")
obj <- CreateSeuratObject(counts = counts, project = "sc",
                          min.cells = 3, min.features = 200)
```

**2. 质控**

```r
obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")   # 人；小鼠用 ^mt-
VlnPlot(obj, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)

obj <- subset(obj, subset = nFeature_RNA > 200 & nFeature_RNA < 6000 & percent.mt < 20)
```

<p>QC 三条线：<strong>nFeature</strong>（检出的基因数，过高常是双细胞）、<strong>nCount</strong>（总计数）、<strong>percent.mt</strong>（线粒体比例，过高说明细胞破损或凋亡）。</p>

**3. 归一化与高变基因**

```r
obj <- NormalizeData(obj)
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 2000)
obj <- ScaleData(obj)
```

**4. 降维与聚类**

```r
obj <- RunPCA(obj, npcs = 30)
ElbowPlot(obj)                                  # 选取用于聚类的 PC 数
obj <- FindNeighbors(obj, dims = 1:20)
obj <- FindClusters(obj, resolution = 0.5)      # resolution 越大，分群越细
obj <- RunUMAP(obj, dims = 1:20)
DimPlot(obj, label = TRUE)
```

**5. 找 marker 基因**

```r
markers <- FindAllMarkers(obj, only.pos = TRUE,
                          min.pct = 0.25, logfc.threshold = 0.25)
top10 <- markers |> group_by(cluster) |> slice_max(avg_log2FC, n = 10)
DoHeatmap(obj, features = top10$gene)
```

**6. 细胞类型注释**

<ul>
  <li><strong>人工注释</strong>：拿已知 marker（如上皮 EPCAM、免疫 PTPRC、T 细胞 CD3D）对照各 cluster 的表达；</li>
  <li><strong>自动注释</strong>：SingleR 用参考数据集打分，CellMarker / PanglaoDB 查 marker 清单。</li>
</ul>

```r
library(SingleR)
pred <- SingleR(test = as.SingleCellExperiment(obj), ref = ref_data, labels = ref_data$label.main)
obj$celltype <- pred$labels
```

**7. 多样本整合（有批次时）**

多个样本不能直接合并聚类，应先整合（Seurat 的 <code>IntegrateLayers</code> 或 Harmony 校正），再做降维聚类。

## 四、结果判读

<ul>
  <li><strong>先看 QC 小提琴图</strong>：若 percent.mt 普遍偏高，说明样本质量差，后面再漂亮的分群也不可信。</li>
  <li><strong>UMAP 只用于展示</strong>：簇间距离不代表真实分化距离，不能用"两点挨得近"来论证关系，定量结论要回到表达值。</li>
  <li><strong>resolution 的选择</strong>：0.5 通常得到大类别；调到 1.0–1.5 会分出亚群。应以 marker 是否可解释为准，而不是"分得越细越好"。</li>
  <li><strong>marker 的特异性</strong>：一个合格 marker 应在目标 cluster 高表达、其他 cluster 几乎不表达（看 avg_log2FC 与 pct.1/pct.2）。</li>
  <li><strong>双细胞假象</strong>：同时表达两类细胞 marker 且 nFeature 偏高的簇，很可能是两个细胞被包进同一个液滴。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>QC 阈值照抄教程</strong>：不同组织、不同建库方式的合理阈值差别很大，必须画图后按数据定。</li>
  <li><strong>不校正批次直接聚类</strong>：得到的簇往往是样本而非细胞类型。</li>
  <li><strong>把亚群当新发现</strong>：resolution 调高会无限分群，每个亚群都需要 marker 支持才能成立。</li>
  <li><strong>注释过于自信</strong>：自动注释只是参考，尤其非模式物种常缺少合适的参考集。</li>
  <li><strong>资源不足</strong>：几万个细胞的整合与聚类很吃内存，笔记本容易崩，建议用服务器或先抽样。</li>
</ul>

## 六、练习

<ol>
  <li>读入一份 10x 数据，绘制 QC 小提琴图并说明你设定的过滤阈值。</li>
  <li>跑 PCA 与 ElbowPlot，说明你选了多少个 PC 及理由。</li>
  <li>用两个不同的 resolution 聚类，比较得到的簇数量差异。</li>
  <li>找出每个簇的前 5 个 marker，挑一簇用已知 marker 推断其细胞类型。</li>
  <li>（选做）用 SingleR 自动注释，比较自动与人工注释结果是否一致。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://satijalab.org/seurat/articles/pbmc3k_tutorial.html" target="_blank" rel="noopener">Seurat 官方 PBMC 教程</a></li>
  <li><a href="https://scanpy.readthedocs.io/en/stable/tutorials.html" target="_blank" rel="noopener">Scanpy 教程</a></li>
  <li><a href="https://www.10xgenomics.com/support/software/cell-ranger" target="_blank" rel="noopener">Cell Ranger 文档</a></li>
  <li><a href="https://bioconductor.org/packages/SingleR/" target="_blank" rel="noopener">SingleR 文档</a></li>
</ul>
