---
title: "Multi-omics Integration: GWAS, Pathways & Gene Mapping"
date: "2026-10-05"
weight: 110
category: "Multi-omics"
meta: "Integration · ~22 min"
draft: "false"
---

<p>One omics answers one question; multi-omics connects "variant — expression — metabolism — phenotype" into a causal chain. This module covers three most-used links: GWAS, pathway enrichment, and unknown-gene mapping.</p>
          <h2>1. GWAS: link variants to traits</h2>
          <p>Genome-wide association scans which SNPs associate with a trait in a population. With PLINK:</p>
          <pre><code>plink --bfile genotype --pheno trait.txt \
  --linear --allow-no-sex --out gwas</code></pre>
          <ul>
            <li>Plot a <strong>Manhattan plot</strong> (per-site −log10(p); peaks = significant) and a <strong>QQ plot</strong> (check inflation);</li>
            <li>Significant hits must be <strong>replicated</strong> in an independent cohort, or they are false positives.</li>
          </ul>
          <h2>2. Pathway enrichment: from gene list to mechanism</h2>
          <p>With a set of differential / significant genes, ask "which pathways are they enriched in". Use clusterProfiler (R) for GO and KEGG:</p>
          <pre><code>library(clusterProfiler)
kk &lt;- enrichKEGG(gene = ids, organism = "hsa", pvalueCutoff = 0.05)
dotplot(kk)</code></pre>
          <p>KEGG shows metabolic / signaling pathways; GO shows biological process / cellular component / molecular function.</p>
          <h2>3. Mapping unknown genes</h2>
          <ul>
            <li><strong>Positional cloning / QTL</strong>: map a trait to a chromosomal interval, then narrow candidates;</li>
            <li><strong>eQTL</strong>: SNP–expression association bridges "significant locus → which gene is affected";</li>
            <li><strong>Colocalization</strong>: if a GWAS peak overlaps an eQTL peak, it strongly suggests that gene is the mechanistic mediator.</li>
          </ul>
          <h2>4. One picture that connects them</h2>
          <p>GWAS finds "where the signal is" → eQTL / expression points "which gene" → KEGG says "which pathway" → experiment confirms. Multi-omics is not piling data; it is using different evidence to corroborate and shrink the hypothesis space.</p>
          <blockquote>The most dangerous error in multi-omics is "correlation as causation". A significant SNP ≠ the gene it regulates is the mechanism gene — expression, interaction and function experiments are still needed.</blockquote>


## Mini-case

Run a PCA on an expression matrix — **pick either R or Python**:

R (PCA, factoextra):

```r
library(FactoMineR); library(factoextra)
mat <- read.csv("expr_matrix.csv", row.names = 1)
pca <- PCA(t(mat), graph = FALSE)
fviz_pca_ind(pca)
```

Python (PCA, sklearn):

```python
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
mat = pd.read_csv("expr_matrix.csv", index_col = 0)
pcs = PCA(n_components = 2).fit_transform(mat.T)
plt.scatter(pcs[:, 0], pcs[:, 1]); plt.show()
```

Observe: samples cluster by treatment/tissue — a sign of batch or biological effect. For differential expression see the R/Python snippets in each module.
