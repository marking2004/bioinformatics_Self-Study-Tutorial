---
title: "Case Study: From One Sequence to a Tree"
date: 2026-10-05
weight: 200
category: "Case Study"
draft: false
---

This module strings the separate topics into one line: we take **one real protein sequence** as the protagonist and walk the full pipeline — "fetch from a database → BLAST for homologs → multiple sequence alignment → build a phylogeny → inspect structure/function → (optional) see how it behaves in expression data". Set up the environment, then run the commands step by step; all example data come from public databases, and the fetch commands below are real and runnable.

## 0. Set up the environment

Most bioinformatics tools are command-line programs; Conda is the easiest way to install them (Windows users: prefer WSL or Git Bash):

```bash
conda create -n bioinfo -c bioconda -c conda-forge blast mafft iqtree2 seqkit
conda activate bioinfo
```

Once activated, `blastp`, `mafft`, `iqtree2` and `seqkit` are directly available.

## 1. Fetch a real sequence (databases / sequence retrieval)

We use human **TP53** (the famous tumor-suppressor gene). Its RefSeq protein accession is `NP_000537`; its UniProt accession is `P04637`. Fetch it with NCBI E-utilities — only `curl` needed, no login:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=NP_000537&rettype=fasta" > tp53_human.fasta
head -1 tp53_human.fasta
```

Expected: a FASTA whose first line looks like `>NP_000537.1 tumor protein p53 [Homo sapiens]`, roughly 393 amino acids. You can also fetch directly from UniProt:

```bash
curl -s "https://rest.uniprot.org/uniprotkb/P04637.fasta" -o tp53_human.fasta
```

> Want a different object to practice on? Replace `NP_000537` with the accession of a gene you care about; if you don't know the accession yet, search the gene name on NCBI / UniProt first.

## 2. BLAST for homologs (sequence analysis)

Use this sequence to find homologs in the nr database:

```bash
blastp -query tp53_human.fasta -db nr -remote -outfmt 6 -max_target_seqs 20 > blast.tsv
head blast.tsv
```

`-outfmt 6` prints a table whose columns are: qacc, sacc, pident %, length, mismatches, gaps, q.start/end, s.start/end, e-value, bit-score.

**How to read it**: high `pident` (e.g. >80%) with a tiny `evalue` (e.g. `0.0`) means close homologs; lower `pident` but still tiny `evalue` means distant homologs or functionally similar proteins. These hits are the raw material for the next alignment.

## 3. Multiple sequence alignment, MSA (MSA & visualization)

For teaching, we align a few TP53 orthologs directly (real UniProt accessions):

```bash
for acc in P04637 P02340 P09867 Q9WU93; do
  curl -s "https://rest.uniprot.org/uniprotkb/$acc.fasta" >> tp53_orthologs.fasta
done
mafft --auto tp53_orthologs.fasta > tp53_orthologs.aln
```

Expected: `tp53_orthologs.aln` is aligned FASTA with equal-length sequences (gaps shown as `-`). Open `.aln` in **Jalview** or **AliView** to see conserved vs. variable positions — the DNA-binding domain is usually highly conserved.

> Prefer your own BLAST hits? Pull the interesting `sacc` values from `blast.tsv` in step 2, build a FASTA the same way, then align.

## 4. A phylogenetic tree (phylogenetics)

Build a tree from the alignment:

```bash
iqtree2 -s tp53_orthologs.aln -m MFP -bb 1000 -nt AUTO
```

Expected: produces `tp53_orthologs.aln.treefile` (Newick format). Open it in **FigTree**, **iTOL** (web), or **ggtree** (see section 6): human/mouse should cluster together, zebrafish and chicken branch more externally — consistent with species evolution, showing TP53 is evolutionarily conserved.

> This "single-gene" tree is the most basic layer; multi-gene and omics-based trees follow the same idea with larger input matrices.

## 5. Structure & functional hotspots (protein analysis / design)

No need to run AlphaFold locally — just download the public prediction:

```bash
curl -s "https://alphafold.ebi.ac.uk/files/AF-P04637-F1-model_v4.cif" -o P04637.cif
```

Open `P04637.cif` in **PyMOL** or **ChimeraX** and focus on the classic hotspot mutations in the DNA-binding domain: **R175, R248, R273** — all frequent TP53 cancer mutations. To go further into "redesign / de novo design", return to the peptide/protein design and structure-prediction modules.

## 6. (Optional) Multi-omics: see it in expression data

To simply visualize a gene's expression across conditions, the data-wrangling / plotting step can be done in **R** or **Python**. Both snippets below do the same thing: read an expression matrix and boxplot TP53.

**R (readr + ggplot2 + ggpubr):**

```r
library(readr); library(ggplot2); library(ggpubr)
mat <- read_csv("expression_matrix.csv")          # rows=genes, cols=samples, plus a group column
p53 <- mat[mat$gene == "TP53", ]
ggplot(p53, aes(x = group, y = expression, fill = group)) +
  geom_boxplot() + stat_compare_means() +
  labs(title = "TP53 expression by group") + theme_minimal()
```

**Python (pandas + seaborn):**

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

> `expression_matrix.csv` comes from your own GEO/ArrayExpress download and cleanup; see the mini-case studies in the Multi-omics and RNA-seq modules for the fetch workflow.

## Summary

One sequence threads through: **database retrieval → BLAST → MSA → phylogenetics → structure**. This pipeline touches about half the modules on this site. The "Mini-case" sections at the end of each module go deeper on single points; for more external tutorials, see "References" in the top nav.

**Sample data / download links**: `tp53_orthologs.fasta` above is generated live by the step-3 commands; you can also download a single protein FASTA directly (e.g. `https://rest.uniprot.org/uniprotkb/P04637.fasta`). All example sequences come from public NCBI / UniProt databases, and the commands are real and runnable.
