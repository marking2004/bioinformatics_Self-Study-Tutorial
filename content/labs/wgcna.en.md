---
title: "Lab 12: Weighted Gene Co-expression Network Analysis (WGCNA)"
date: "2026-10-10"
weight: 120
category: "Multi-omics"
meta: "Omics · ~60 min"
module: "multi-omics"
draft: false
summary: "Differential expression looks at single genes; WGCNA looks at modules of genes. This lab builds a network with the R package WGCNA, detects modules, relates them to traits and picks hub genes."
---

> Module: [Multi-omics Integration](../posts/multi-omics.html)

## 1. Goals

<ul>
  <li>Understand the basic units: module, eigengene and connectivity;</li>
  <li>Run soft-threshold selection, module detection and module merging;</li>
  <li>Relate modules to phenotypic traits and extract <strong>hub genes</strong>;</li>
  <li>Appreciate how sample size and outliers affect the outcome.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>WGCNA (R package)</td><td>network construction and modules</td><td><a href="https://horvath.genetics.ucla.edu/html/CoexpressionNetwork/Rpackages/WGCNA/" target="_blank" rel="noopener">tutorials</a></td></tr>
    <tr><td>Cytoscape</td><td>network visualisation</td><td><a href="https://cytoscape.org/" target="_blank" rel="noopener">cytoscape.org</a></td></tr>
    <tr><td>clusterProfiler</td><td>module annotation</td><td><a href="https://bioconductor.org/packages/clusterProfiler/" target="_blank" rel="noopener">clusterProfiler</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Prepare the expression matrix**

<p>Use <strong>at least 15–20 samples</strong> (fewer makes the network unstable) and filter low-expressed genes first:</p>

```r
library(WGCNA)
dat <- read.delim("expr_matrix.tsv", row.names = 1)
dat <- dat[rowSums(dat > 1) >= 3, ]        # drop barely expressed genes
```

**2. Check for outlier samples**

```r
sampleTree <- hclust(dist(t(dat)), method = "average")
plot(sampleTree)                            # remove clearly outlying branches
```

**3. Choose the soft threshold**

```r
powers <- c(1:20)
sft <- pickSoftThreshold(dat, powerVector = powers, verbose = 5)
plot(sft$fitIndices[,1], -sign(sft$fitIndices[,3]) * sft$fitIndices[,2],
     xlab = "Soft Threshold (power)", ylab = "Scale Free Topology Model Fit")
```

Pick the <strong>smallest power whose scale-free fit index reaches about 0.8</strong> (commonly 6–12).

**4. Build the network and detect modules**

```r
net <- blockwiseModules(dat, power = sft$powerEstimate,
                        TOMType = "unsigned", minModuleSize = 30,
                        reassignThreshold = 0, mergeCutHeight = 0.25,
                        numericLabels = TRUE, verbose = 3)
table(net$colors)                           # genes per module
MEs <- net$MEs
```

**5. Relate modules to traits**

```r
trait <- read.delim("traits.tsv", row.names = 1)
modTrait <- cor(MEs, trait, use = "p")
modTraitP <- corPvalueStudent(modTrait, nrow(dat))
labeledHeatmap(Matrix = modTrait, xLabels = colnames(trait),
               yLabels = names(MEs), colorLabels = FALSE)
```

**6. Hub genes**

```r
ADJ <- adjacency(dat, power = sft$powerEstimate)
k <- intramodularConnectivity(ADJ, net$colors)
hub <- rownames(k)[order(-k$kWithin, )[1:20]]     # top 20 by connectivity
```

**7. Export to Cytoscape**

```r
TOM <- TOMsimilarityFromExpr(dat, power = sft$powerEstimate)
exportNetworkToCytoscape(TOM, edgeFile = "edges.txt",
                         nodeFile = "nodes.txt", threshold = 0.15)
```

## 4. Reading the results

<ul>
  <li><strong>The threshold curve</strong>: fit index rises with power then plateaus. Take the value at roughly 0.8. If it never gets there, the data do not fit a scale-free network — check heterogeneity and gene filtering.</li>
  <li><strong>Number of modules</strong>: in <code>table(net$colors)</code> the grey module holds unassigned genes; a large grey share means the network did not build well.</li>
  <li><strong>Module-trait correlation</strong>: read the correlation and its p-value together. Only modules with large magnitude and small p are worth chasing, and correlation is <strong>statistical association, not causation</strong>.</li>
  <li><strong>Hub genes</strong>: the most connected genes within a module are often regulatory cores, but they are <strong>candidates</strong> needing experimental or independent-data support.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Too few samples</strong>: fewer than 15 makes results hard to reproduce — the most common reviewer objection to WGCNA.</li>
  <li><strong>Skipping outlier detection</strong>: one aberrant sample distorts the whole correlation matrix.</li>
  <li><strong>Uncorrected batch effects</strong>: modules may track batch rather than biology; run PCA first.</li>
  <li><strong>Copied parameters</strong>: <code>power</code>, <code>minModuleSize</code> and <code>mergeCutHeight</code> need tuning per dataset.</li>
  <li><strong>Treating modules as pathways</strong>: a module is a co-expression cluster; enrichment tells you what it might do.</li>
</ul>

## 6. Exercises

<ol>
  <li>Cluster samples on an expression matrix of ≥15 samples and decide whether any outliers must go.</li>
  <li>Run <code>pickSoftThreshold</code>; record the power you chose and its fit index.</li>
  <li>Build the network; report the number of modules and the share of grey genes.</li>
  <li>Produce a module-trait heatmap and name the strongest significant module.</li>
  <li>(Optional) Enrich that module with GO and export the top 20 hub genes.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://horvath.genetics.ucla.edu/html/CoexpressionNetwork/Rpackages/WGCNA/Tutorials/" target="_blank" rel="noopener">WGCNA tutorial collection</a></li>
  <li><a href="https://cytoscape.org/documentation_users.html" target="_blank" rel="noopener">Cytoscape documentation</a></li>
</ul>
