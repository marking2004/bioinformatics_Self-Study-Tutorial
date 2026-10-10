---
title: "多组学联合分析：GWAS、通路与基因定位"
date: "2026-10-05"
weight: 110
category: "多组学"
meta: "整合 · 约 22 分钟"
draft: "false"
summary: "单个组学回答一个问题；多组学把'变异—表达—代谢—表型'连成因果链。本模块讲三件最常用的串联：GWAS、通路富集、未知基因定位。"
---

<p>单个组学回答一个问题；多组学把"变异—表达—代谢—表型"连成因果链。本模块讲三件最常用的串联：GWAS、通路富集、未知基因定位。</p>
          <h2>1. GWAS：把变异和性状连起来</h2>
          <p>全基因组关联分析在群体中扫描哪些 SNP 与某性状显著相关。常用 PLINK：</p>
          <pre><code>plink --bfile genotype --pheno trait.txt \
  --linear --allow-no-sex --out gwas</code></pre>
          <ul>
            <li>结果画 <strong>曼哈顿图</strong>（每位点 −log10(p)，尖峰 = 显著位点）与 <strong>QQ 图</strong>（看是否通胀）；</li>
            <li>显著位点要在独立群体里<strong>重复验证</strong>，否则易假阳性。</li>
          </ul>
          <h2>2. 通路富集：从基因列表到机制</h2>
          <p>拿到一组差异 / 显著基因后，问"它们富集在哪条通路"。用 clusterProfiler（R）做 GO 与 KEGG：</p>
          <pre><code>library(clusterProfiler)
kk &lt;- enrichKEGG(gene = ids, organism = "hsa", pvalueCutoff = 0.05)
dotplot(kk)</code></pre>
          <p>KEGG 看代谢 / 信号通路，GO 看生物过程 / 细胞组分 / 分子功能。</p>
          <h2>3. 未知基因定位</h2>
          <ul>
            <li><strong>定位克隆 / QTL</strong>：把性状定位到染色体区间，再缩小候选基因；</li>
            <li><strong>eQTL</strong>：SNP 与基因表达量的关联，帮"显著位点 → 哪个基因受影响"建桥；</li>
            <li><strong>共定位（colocalization）</strong>：若 GWAS 峰与 eQTL 峰重叠，强烈提示该基因是机制中介。</li>
          </ul>
          <h2>4. 把它们连起来的一张图</h2>
          <p>GWAS 找"哪里有信号" → eQTL / 表达数据指"哪个基因" → KEGG 说"走哪条通路" → 实验验证。多组学不是堆数据，而是用不同证据互相佐证、缩小假设空间。</p>
          <blockquote>多组学最危险的错误是"相关当因果"。一个 SNP 显著，不等于它控制的基因就是机制基因——还需要表达、互作、功能实验来坐实。</blockquote>


## 迷你实战

拿一个表达矩阵做 PCA，**R 与 Python 任选其一**：

R（PCA，factoextra）：

```r
library(FactoMineR); library(factoextra)
mat <- read.csv("expr_matrix.csv", row.names = 1)
pca <- PCA(t(mat), graph = FALSE)
fviz_pca_ind(pca)
```

Python（PCA，sklearn）：

```python
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
mat = pd.read_csv("expr_matrix.csv", index_col = 0)
pcs = PCA(n_components = 2).fit_transform(mat.T)
plt.scatter(pcs[:, 0], pcs[:, 1]); plt.show()
```

观察：样本按处理/组织聚成簇，说明批次或生物学效应明显。差异表达见各模块的 R/Python 片段。
