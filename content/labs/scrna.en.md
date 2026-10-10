---
title: "Lab 14: Single-cell Transcriptome Analysis"
date: "2026-10-10"
weight: 140
category: "Multi-omics"
meta: "Omics · ~70 min"
module: "multi-omics"
draft: false
summary: "Single-cell work replaces a tissue average with per-cell resolution. This lab runs Seurat through QC, dimensionality reduction, clustering, markers and cell-type annotation, and flags doublets, batch effects and resolution choices."
---

> Module: [Multi-omics Integration](../posts/multi-omics.html)

## 1. Goals

<ul>
  <li>Understand single-cell matrices: extremely sparse, barcode/UMI counts;</li>
  <li>Run QC, normalisation, dimensionality reduction, clustering and markers with <strong>Seurat</strong>;</li>
  <li>Name clusters using known markers or automated annotation;</li>
  <li>See how doublets, batch effects and resolution determine whether the result holds.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>Seurat (R)</td><td>mainstream single-cell framework</td><td><a href="https://satijalab.org/seurat/" target="_blank" rel="noopener">satijalab.org</a></td></tr>
    <tr><td>Scanpy (Python)</td><td>Python equivalent</td><td><a href="https://scanpy.readthedocs.io/" target="_blank" rel="noopener">scanpy</a></td></tr>
    <tr><td>Cell Ranger (10x)</td><td>raw data quantification</td><td><a href="https://www.10xgenomics.com/support/software/cell-ranger" target="_blank" rel="noopener">10x Genomics</a></td></tr>
    <tr><td>SingleR / CellMarker</td><td>cell-type annotation</td><td><a href="https://bioconductor.org/packages/SingleR/" target="_blank" rel="noopener">SingleR</a> · <a href="http://117.50.127.228/CellMarker/" target="_blank" rel="noopener">CellMarker</a></td></tr>
    <tr><td>Harmony</td><td>batch correction</td><td><a href="https://github.com/immunogenomics/harmony" target="_blank" rel="noopener">Harmony</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Load the data**

```r
library(Seurat)
counts <- Read10X(data.dir = "filtered_feature_bc_matrix/")
obj <- CreateSeuratObject(counts = counts, project = "sc",
                          min.cells = 3, min.features = 200)
```

**2. Quality control**

```r
obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")   # human; ^mt- for mouse
VlnPlot(obj, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)

obj <- subset(obj, subset = nFeature_RNA > 200 & nFeature_RNA < 6000 & percent.mt < 20)
```

<p>Three QC lines: <strong>nFeature</strong> (genes detected; very high suggests doublets), <strong>nCount</strong> (total counts) and <strong>percent.mt</strong> (mitochondrial fraction; high means damaged or dying cells).</p>

**3. Normalisation and variable features**

```r
obj <- NormalizeData(obj)
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 2000)
obj <- ScaleData(obj)
```

**4. Reduce dimensions and cluster**

```r
obj <- RunPCA(obj, npcs = 30)
ElbowPlot(obj)                                  # choose how many PCs to use
obj <- FindNeighbors(obj, dims = 1:20)
obj <- FindClusters(obj, resolution = 0.5)      # higher resolution, finer clusters
obj <- RunUMAP(obj, dims = 1:20)
DimPlot(obj, label = TRUE)
```

**5. Marker genes**

```r
markers <- FindAllMarkers(obj, only.pos = TRUE,
                          min.pct = 0.25, logfc.threshold = 0.25)
top10 <- markers |> group_by(cluster) |> slice_max(avg_log2FC, n = 10)
DoHeatmap(obj, features = top10$gene)
```

**6. Annotate cell types**

<ul>
  <li><strong>Manual</strong>: compare known markers with cluster expression (e.g. EPCAM for epithelium, PTPRC for immune, CD3D for T cells);</li>
  <li><strong>Automated</strong>: SingleR scores against reference datasets; CellMarker / PanglaoDB supply marker lists.</li>
</ul>

```r
library(SingleR)
pred <- SingleR(test = as.SingleCellExperiment(obj), ref = ref_data, labels = ref_data$label.main)
obj$celltype <- pred$labels
```

**7. Integrate multiple samples**

Do not simply merge and cluster. Integrate first (Seurat's <code>IntegrateLayers</code> or Harmony), then reduce and cluster.

## 4. Reading the results

<ul>
  <li><strong>Read the QC violin plots first</strong>: if percent.mt is high across the board, the sample is poor and no amount of pretty clustering rescues it.</li>
  <li><strong>UMAP is display only</strong>: distances between clusters are not real differentiation distances. Do not argue relationships from proximity; quantitative claims go back to expression values.</li>
  <li><strong>Choosing resolution</strong>: 0.5 usually yields broad classes; 1.0–1.5 resolves subtypes. Let marker interpretability decide, not "finer is better".</li>
  <li><strong>Marker specificity</strong>: a good marker is high in the target cluster and near-zero elsewhere (check avg_log2FC and pct.1/pct.2).</li>
  <li><strong>Doublet artefacts</strong>: a cluster expressing markers of two lineages with high nFeature is probably two cells in one droplet.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Copying QC thresholds</strong>: reasonable values differ hugely across tissues and chemistries. Plot first, then decide.</li>
  <li><strong>Clustering without batch correction</strong>: the clusters become samples rather than cell types.</li>
  <li><strong>Calling every subcluster a discovery</strong>: raising resolution splits indefinitely; each subcluster needs marker support.</li>
  <li><strong>Over-confident annotation</strong>: automated labels are a starting point, and non-model species often lack a suitable reference.</li>
  <li><strong>Insufficient resources</strong>: integrating and clustering tens of thousands of cells is memory-hungry; use a server or subsample first.</li>
</ul>

## 6. Exercises

<ol>
  <li>Load a 10x dataset, draw QC violin plots and justify your filters.</li>
  <li>Run PCA and ElbowPlot; state how many PCs you used and why.</li>
  <li>Cluster at two resolutions and compare cluster counts.</li>
  <li>Find the top five markers per cluster and infer a cell type for one cluster.</li>
  <li>(Optional) Annotate with SingleR and compare with your manual calls.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://satijalab.org/seurat/articles/pbmc3k_tutorial.html" target="_blank" rel="noopener">Seurat PBMC tutorial</a></li>
  <li><a href="https://scanpy.readthedocs.io/en/stable/tutorials.html" target="_blank" rel="noopener">Scanpy tutorials</a></li>
  <li><a href="https://www.10xgenomics.com/support/software/cell-ranger" target="_blank" rel="noopener">Cell Ranger documentation</a></li>
  <li><a href="https://bioconductor.org/packages/SingleR/" target="_blank" rel="noopener">SingleR documentation</a></li>
</ul>
