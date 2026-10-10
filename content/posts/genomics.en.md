---
title: "Nucleic-acid Analysis & Genomics"
date: "2026-10-05"
weight: 60
category: "Genomics"
meta: "Omics · ~25 min"
draft: "false"
---

<p>Genomics asks what whole DNA / whole-sequence sets tell us. This module strings together common sub-topics so you can pick what you need.</p>
          <h2>1. Sequencing data processing</h2>
          <ul>
            <li><strong>QC &amp; filtering</strong>: fastp (adapter trimming, QC, clipping in one step);</li>
            <li><strong>Assembly</strong>: SPAdes / SOAPdenovo (short read), Canu / Flye (long read);</li>
            <li><strong>Map to reference</strong>: BWA (short), minimap2 (long / cross-species).</li>
          </ul>
          <pre><code>fastp -i r1.fq -o c1.fq -I r2.fq -O c2.fq
bwa mem ref.fa c1.fq c2.fq | samtools sort &gt; sample.bam</code></pre>
          <h2>2. Synteny analysis</h2>
          <p>Compare which blocks of two genomes correspond and whether rearrangements occurred. Tools: MCscan (Python), JDart, SynVisio (visualization). Used for chromosomal rearrangements after speciation.</p>
          <h2>3. Gene / protein family analysis</h2>
          <ul>
            <li><strong>OrthoFinder</strong>: infer ortho-/paralogroups, output families and phylogenies;</li>
            <li><strong>Pfam / InterPro</strong>: family and domain annotation;</li>
            <li><strong>CAFE</strong>: test family expansion / contraction (with a species tree).</li>
          </ul>
          <h2>4. SNPs, markers and genetic diversity</h2>
          <ul>
            <li><strong>Calling</strong>: GATK (standard), freebayes;</li>
            <li><strong>Population stats</strong>: vcftools / PLINK for π, Fst, Tajima's D — selection signals and diversity;</li>
            <li><strong>Molecular markers</strong>: SSR, SNP arrays for breeding and fingerprinting.</li>
          </ul>
          <pre><code>vcftools --vcf snps.vcf --weir-fst-pop popA.txt \
  --weir-fst-pop popB.txt --out fst</code></pre>
          <h2>5. Various small RNAs</h2>
          <ul>
            <li><strong>miRNA</strong>: miRBase annotation, sRNAbench / miRDeep2 for novel miRNA;</li>
            <li><strong>siRNA / piRNA</strong>: length distribution and origin (transposons / heterochromatin);</li>
            <li><strong>lncRNA</strong>: filter by length, exon structure, coding potential (CPC2 / CNCI).</li>
          </ul>
          <blockquote>The pitfall in genomics is "wrong data": contamination, heterozygosity, batch, sample mix-up. Before any conclusion, run basic QC and sample correlation (PCA).</blockquote>


## Mini-case

Inspect a BAM with samtools (you need an alignment first):

```bash
samtools flagstat aln.bam
samtools idxstats aln.bam
```

Observe: mapped % in `flagstat` is the alignment rate; `idxstats` gives per-reference coverage depth. Use `seqkit` the same way for FASTA/A.
