---
title: "Lab 11: RNA-seq from QC to Enrichment"
date: "2026-10-10"
weight: 110
category: "Transcriptomics"
meta: "Omics · ~70 min"
module: "rna-seq"
draft: false
summary: "Transcriptomics is the omics analysis undergraduates meet most. This lab runs the full chain: QC, alignment or alignment-free quantification, counting, differential expression and enrichment — plus the usual trip-ups: FPKM, replicates and batch effects."
---

> Module: [RNA-seq Analysis](../posts/rna-seq.html)

## 1. Goals

<ul>
  <li>Know the standard RNA-seq chain and what each step consumes and produces;</li>
  <li>Run QC, alignment (or alignment-free quantification) and gene-level counting;</li>
  <li>Do differential expression with <strong>DESeq2</strong> and interpret padj and log2FC;</li>
  <li>Run GO / KEGG enrichment with <strong>clusterProfiler</strong> and understand the background gene set.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>fastp / FastQC / MultiQC</td><td>QC and summarised reports</td><td><a href="https://github.com/OpenGene/fastp" target="_blank" rel="noopener">fastp</a> · <a href="https://multiqc.info/" target="_blank" rel="noopener">MultiQC</a></td></tr>
    <tr><td>HISAT2 / STAR</td><td>genome alignment</td><td><a href="https://daehwankimlab.github.io/hisat2/" target="_blank" rel="noopener">HISAT2</a> · <a href="https://github.com/alexdobin/STAR" target="_blank" rel="noopener">STAR</a></td></tr>
    <tr><td>Salmon / kallisto</td><td>alignment-free quantification</td><td><a href="https://salmon.readthedocs.io/" target="_blank" rel="noopener">Salmon</a> · <a href="https://pachterlab.github.io/kallisto/" target="_blank" rel="noopener">kallisto</a></td></tr>
    <tr><td>featureCounts</td><td>gene-level counting</td><td><a href="https://subread.sourceforge.net/" target="_blank" rel="noopener">Subread</a></td></tr>
    <tr><td>DESeq2 / edgeR</td><td>differential expression</td><td><a href="https://bioconductor.org/packages/DESeq2/" target="_blank" rel="noopener">DESeq2</a></td></tr>
    <tr><td>clusterProfiler</td><td>GO / KEGG enrichment</td><td><a href="https://bioconductor.org/packages/clusterProfiler/" target="_blank" rel="noopener">clusterProfiler</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Quality control**

```bash
fastp -i R1.fq.gz -I R2.fq.gz -o clean_R1.fq.gz -O clean_R2.fq.gz \
      --detect_adapter_for_pe --cut_tail --cut_mean_quality 20 \
      --html qc/sample.html
multiqc qc/ -o qc/multiqc_report.html      # read this first for multiple samples
```

**2. Route A: align to the genome**

```bash
hisat2-build genome.fa genome_idx                      # once only
hisat2 -x genome_idx -1 clean_R1.fq.gz -2 clean_R2.fq.gz -S aln.sam -p 8
samtools sort -@ 4 -o sorted.bam aln.sam && samtools index sorted.bam
featureCounts -T 8 -p -a annotation.gtf -o counts.txt sorted.bam
```

**3. Route B: alignment-free quantification (faster)**

```bash
salmon index -t transcripts.fa -i tx_idx
salmon quant -i tx_idx -l A -1 clean_R1.fq.gz -2 clean_R2.fq.gz -o quant/sample
```

<p>With a good reference transcriptome, Salmon is far faster. Choose the alignment route when you need splicing, novel transcripts or isoform-level detail.</p>

**4. Differential expression with DESeq2**

```r
library(DESeq2)
cts <- read.delim("counts.txt", row.names = 1, check.names = FALSE)
cts <- cts[, 6:ncol(cts)]                       # drop featureCounts annotation columns
coldata <- data.frame(condition = factor(c("ctrl","ctrl","treat","treat")))
rownames(coldata) <- colnames(cts)

dds <- DESeqDataSetFromMatrix(cts, coldata, ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast = c("condition", "treat", "ctrl"))
res <- res[order(res$padj), ]
write.csv(as.data.frame(res), "DEG.csv")

plotPCA(vst(dds), intgroup = "condition")
```

**5. Enrichment**

```r
library(clusterProfiler)
library(org.At.tair.db)                        # Arabidopsis; org.Hs.eg.db for human
deg <- rownames(res[res$padj < 0.05 & abs(res$log2FoldChange) > 1, ])

ego <- enrichGO(gene = deg, OrgDb = org.At.tair.db, keyType = "TAIR",
                ont = "BP", pAdjustMethod = "BH", qvalueCutoff = 0.05)
dotplot(ego, showCategory = 20)

kegg <- enrichKEGG(gene = deg, organism = "ath", pAdjustMethod = "BH", qvalueCutoff = 0.05)
```

## 4. Reading the results

<ul>
  <li><strong>Alignment rate</strong>: total mapping should usually exceed 70–90%. Lower suggests contamination, a wrong reference or untrimmed adapters; a high <strong>multi-mapping rate</strong> points to repeats or gene families.</li>
  <li><strong>Use raw counts</strong>: DESeq2 and edgeR normalise internally, so feed them raw counts. <strong>FPKM/TPM must not be used as input.</strong></li>
  <li><strong>Read padj, not pvalue</strong>: with tens of thousands of genes tested simultaneously, multiple-testing correction is mandatory. A common cut-off is <code>padj &lt; 0.05 and |log2FC| &gt; 1</code>.</li>
  <li><strong>PCA before conclusions</strong>: if samples cluster by batch instead of group, you have a <strong>batch effect</strong>. Add batch to the design formula, or your DE list is a list of batch differences.</li>
  <li><strong>Three things in enrichment</strong>: corrected qvalue, the number of genes hitting the term (Count), and whether the <strong>background set</strong> is right — it should be all detected genes, not the whole genome.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Too few biological replicates</strong>: at least three per group. With n=1 dispersion cannot be estimated and DESeq2 output is meaningless; n=2 is highly unstable.</li>
  <li><strong>Running DE on FPKM/TPM</strong>: the most common mistake. Those metrics are for display, not for statistical testing.</li>
  <li><strong>Mismatched annotation and genome</strong>: a GTF from a different build sends many reads to "no gene" territory.</li>
  <li><strong>Wrong enrichment background</strong>: enriching the DE list with no background inflates certain terms.</li>
  <li><strong>Treating enrichment as a conclusion</strong>: enrichment yields <strong>hypotheses</strong>. Function still needs an experiment.</li>
</ul>

## 6. Exercises

<ol>
  <li>Run fastp and MultiQC on a paired-end dataset; report reads before/after and Q20/Q30.</li>
  <li>Align with HISAT2; report mapping and multi-mapping rates and say whether the reference should change.</li>
  <li>Count with featureCounts and check that library totals are comparable across samples.</li>
  <li>Run a two-group DESeq2 comparison; report up- and down-regulated gene counts at padj &lt; 0.05.</li>
  <li>(Optional) Enrich the DE genes with GO, explain one term biologically, and state the limits of your analysis.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://bioconductor.org/packages/DESeq2/vignettes/DESeq2.html" target="_blank" rel="noopener">DESeq2 vignette</a></li>
  <li><a href="https://yulab-smu.top/biomedical-knowledge-mining-book/" target="_blank" rel="noopener">clusterProfiler book</a></li>
  <li><a href="https://salmon.readthedocs.io/en/latest/" target="_blank" rel="noopener">Salmon documentation</a></li>
  <li><a href="https://multiqc.info/" target="_blank" rel="noopener">MultiQC</a></li>
</ul>
