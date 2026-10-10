---
title: "综合实战：从一条序列到一棵树"
date: 2026-10-05
weight: 200
category: "综合实战"
draft: false
---

这一个模块把前面分散的知识点串成一条线：用一条**真实的蛋白质序列**当主角，走完"从数据库取序列 → BLAST 找同源 → 多序列比对 → 建系统发育树 → 看结构功能 →（可选）看它在表达数据里的表现"的完整流程。建议先装好环境，再照着命令一步步跑；所有示例数据都来自公开数据库，命令里给的是真实可运行的取数方式。

## 0. 准备环境

生信工具大多是命令行程序，用 Conda 安装最省事（Windows 用户建议先用 WSL 或 Git Bash）：

```bash
# 安装 Miniconda 后，建一个独立环境
conda create -n bioinfo -c bioconda -c conda-forge blast mafft iqtree2 seqkit
conda activate bioinfo
```

环境激活后，`blastp`、`mafft`、`iqtree2`、`seqkit` 就都能直接用了。

## 1. 取一条真实序列（数据库 / 序列获取）

以人源 **TP53**（著名的肿瘤抑制基因）为例。它的 RefSeq 蛋白编号是 `NP_000537`，UniProt 编号是 `P04637`。用 NCBI 的 E-utilities 取序列，只需 `curl`，不用登录：

```bash
# 从 NCBI 取人源 TP53 蛋白 FASTA
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=NP_000537&rettype=fasta" > tp53_human.fasta
head -1 tp53_human.fasta
```

预期：得到一段 FASTA，第一行类似 `>NP_000537.1 tumor protein p53 [Homo sapiens]`，序列约 393 个氨基酸。也可以直接从 UniProt 取：

```bash
curl -s "https://rest.uniprot.org/uniprotkb/P04637.fasta" -o tp53_human.fasta
```

> 想换个对象练手？把 `NP_000537` 换成你感兴趣基因的 accession 即可；不知道 accession 就先去 NCBI / UniProt 网站搜基因名。

## 2. BLAST 找同源蛋白（序列分析）

拿这条序列去 nr 库里找同源：

```bash
blastp -query tp53_human.fasta -db nr -remote -outfmt 6 -max_target_seqs 20 > blast.tsv
head blast.tsv
```

`-outfmt 6` 输出的是表格，列依次是：查询名、命中名、一致度%、比对长度、错配、空缺、查询起止、命中起止、e-value、bit-score。

**怎么读结果**：`pident` 高（比如 >80%）、`evalue` 极小（如 `0.0`）的是近缘同源；`pident` 较低但 `evalue` 仍很小，说明是远缘同源或功能相似的蛋白。这些命中的序列，就是下一步做比对的原料。

## 3. 多序列比对 MSA（多序列比对与可视化）

教学起见，这里直接取几个物种的 TP53 同源蛋白做比对（真实 accession 来自 UniProt）：

```bash
# 取若干个物种的 TP53 同源蛋白（人/小鼠/斑马鱼/鸡 仅为示例）
for acc in P04637 P02340 P09867 Q9WU93; do
  curl -s "https://rest.uniprot.org/uniprotkb/$acc.fasta" >> tp53_orthologs.fasta
done
mafft --auto tp53_orthologs.fasta > tp53_orthologs.aln
```

预期：`tp53_orthologs.aln` 是对齐后的 FASTA，所有序列长度一致（缺口用 `-` 填充）。把 `.aln` 拖进 **Jalview** 或 **AliView** 就能看到保守位点和变异位点——DNA 结合域通常高度保守。

> 想用自己 BLAST 命中的序列？把第 2 步 `blast.tsv` 里感兴趣的 `sacc` 取出来，按同样方式拼成 FASTA 再比对即可。

## 4. 系统发育树（系统发育分析）

基于上一步的比对建树：

```bash
iqtree2 -s tp53_orthologs.aln -m MFP -bb 1000 -nt AUTO
```

预期：会生成 `tp53_orthologs.aln.treefile`（Newick 格式）。用 **FigTree**、**iTOL**（网页）或 **ggtree**（见第 6 节）打开：人/小鼠应该聚在一起，斑马鱼、鸡更靠外——这和物种演化关系一致，说明 TP53 在演化上很保守。

> 按数据层次，这棵"基于单基因"的树是最基础的一层；多基因联合、基于组学数据的树思路类似，只是输入的对齐矩阵更大。

## 5. 结构与功能热点（蛋白质分析 / 设计）

不用本地跑 AlphaFold，直接下载公开预测结构：

```bash
curl -s "https://alphafold.ebi.ac.uk/files/AF-P04637-F1-model_v4.cif" -o P04637.cif
```

用 **PyMOL** 或 **ChimeraX** 打开 `P04637.cif`，重点看 DNA 结合域里的几个经典热点突变：**R175、R248、R273**——它们都是 TP53 高频致癌突变位点。想进一步做"改造/从头设计"，可回到"肽与蛋白质合理设计""蛋白质结构预测"模块深入。

## 6.（可选）多组学：看它在表达数据里的表现

如果只是想直观看看某个基因在不同条件下的表达差异，数据分析/作图环节用 **R** 或 **Python** 都可以。下面两份代码做同一件事：读一个表达矩阵、画 TP53 的箱线图。

**R（readr + ggplot2 + ggridges/ggpubr）：**

```r
library(readr); library(ggplot2); library(ggpubr)
mat <- read_csv("expression_matrix.csv")          # 行=基因, 列=样本, 含 group 列
p53 <- mat[mat$gene == "TP53", ]
ggplot(p53, aes(x = group, y = expression, fill = group)) +
  geom_boxplot() + stat_compare_means() +
  labs(title = "TP53 expression by group") + theme_minimal()
```

**Python（pandas + seaborn）：**

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

mat = pd.read_csv("expression_matrix.csv")
p53 = mat[mat["gene"] == "TP53"]
sns.boxplot(data=p53, x="group", y="expression")
plt.title("TP53 expression by group")
plt.show()
```

> 这里的 `expression_matrix.csv` 来自你自己的 GEO/ArrayExpress 下载与整理；具体取数流程见"多组学联合""RNA-seq 实战"模块的迷你实战。

## 小结

一条序列，串起了：**数据库获取 → BLAST → MSA → 系统发育 → 结构**。这套流程几乎覆盖了本站点一半的模块。后续每个模块末尾的"迷你实战"会就单点继续加深；想找更多外部教程，见站点顶部的"参考资料"。

**样本数据 / 下载链接**：上面的 `tp53_orthologs.fasta` 由第 3 步命令现场生成；也可直接下载单个蛋白 FASTA（如 `https://rest.uniprot.org/uniprotkb/P04637.fasta`）。所有示例序列均来自 NCBI / UniProt 公开库，命令真实可运行。
