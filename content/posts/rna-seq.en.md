---
title: "RNA-seq in Practice: From Reads to Differential Genes"
date: "2026-10-05"
weight: 70
category: "Omics"
meta: "Omics · ~20 min"
draft: "false"
---

<p>RNA-seq answers one question: "which genes are expressed more / less under which condition?" This lesson walks a slim but real pipeline — from raw reads (fastq) to differentially expressed genes, and your first volcano plot.</p>
          <h2>1. Pipeline overview</h2>
          <ul>
            <li>raw reads (fastq) → <strong>QC</strong> (FastQC)</li>
            <li>→ <strong>align</strong> to a reference genome (HISAT2)</li>
            <li>→ <strong>quantify</strong> (featureCounts)</li>
            <li>→ <strong>differential analysis</strong> (DESeq2) → visualize</li>
          </ul>
          <h2>2. QC: is the data clean?</h2>
          <pre><code>fastqc sample_R1.fastq.gz sample_R2.fastq.gz
multiqc .     # aggregate reports from all samples into one page</code></pre>
          <p>Watch for per-base quality decay along the read and adapter contamination. Dirty data left untreated ruins everything downstream.</p>
          <h2>3. Alignment and quantification</h2>
          <pre><code># align to reference, write sorted bam
hisat2 -x genome_index -1 sample_R1.fq -2 sample_R2.fq \
  | samtools sort -o sample.bam

# count reads per gene (gtf annotation)
featureCounts -a genes.gtf -o counts.txt sample.bam</code></pre>
          <h2>4. Differential expression (R + DESeq2)</h2>
          <pre><code>library(DESeq2)
dds <- DESeqDataSetFromMatrix(countData, colData, ~ condition)
dds <- DESeq(dds)
res <- results(dds, alpha = 0.05)
summary(res)        # how many genes up / down</code></pre>
          <p><code>alpha = 0.05</code> is the significance cutoff; DESeq2 does normalization and multiple-testing correction for you.</p>
          <h2>5. Your first volcano plot</h2>
          <pre><code>library(ggplot2)
res$log10p <- -log10(res$padj)
ggplot(res, aes(log2FoldChange, log10p)) +
  geom_point(alpha = .4) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed")</code></pre>
          <p>x is fold-change (log2), y is significance (−log10 adjusted p). The upper-right / lower-right points are the candidates worth chasing.</p>
          <h2>Summary</h2>
          <p>An RNA-seq pipeline hides many details (batch effects, normalization, multiple testing); this lesson only sketches the skeleton. But once you run it yourself, papers and methods talks stop sounding like jargon.</p>


## Mini-case

Check quality with fastqc, then quantify with salmon (use your own paired-end data):

```bash
fastqc reads_1.fastq.gz reads_2.fastq.gz
salmon index -t transcriptome.fa -i index
salmon quant -i index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -o quant
```

Observe: each row of `quant/quant.sf` gives `NumReads` / `TPM` per transcript. Download real SRR data from GEO and run the same pipeline.
