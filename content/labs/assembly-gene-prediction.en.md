---
title: "Lab 9: Sequence Assembly and Gene Prediction"
date: "2026-10-10"
weight: 90
category: "Genomics"
meta: "Omics · ~55 min"
module: "genomics"
draft: false
summary: "Sequencing gives you millions of short reads; you must assemble them before you can locate genes. This lab runs QC, assembly, evaluation, gene prediction and ORF finding, and explains how far to trust the output."
---

> Module: [Nucleic-acid Analysis & Genomics](../posts/genomics.html)

## 1. Goals

<ul>
  <li>Understand how reads become contigs and scaffolds, and the built-in limits of that process;</li>
  <li>Assemble quality with QUAST and BUSCO and read N50 correctly;</li>
  <li>Contrast <strong>ab initio</strong> with <strong>evidence-based</strong> gene prediction and run both;</li>
  <li>Find ORFs and translate them, online and from the command line.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>fastp / FastQC</td><td>QC and filtering</td><td><a href="https://github.com/OpenGene/fastp" target="_blank" rel="noopener">fastp</a> · <a href="https://www.bioinformatics.babraham.ac.uk/projects/fastqc/" target="_blank" rel="noopener">FastQC</a></td></tr>
    <tr><td>SPAdes / Flye</td><td>short-read / long-read assembly</td><td><a href="https://cab.spbu.ru/software/spades/" target="_blank" rel="noopener">SPAdes</a> · <a href="https://github.com/fenderglass/Flye" target="_blank" rel="noopener">Flye</a></td></tr>
    <tr><td>QUAST / BUSCO</td><td>assembly quality and completeness</td><td><a href="https://quast.sourceforge.net/quast" target="_blank" rel="noopener">QUAST</a> · <a href="https://busco.ezlab.org/" target="_blank" rel="noopener">BUSCO</a></td></tr>
    <tr><td>Prodigal / Augustus</td><td>prokaryotic / eukaryotic gene finding</td><td><a href="https://github.com/hyattpd/Prodigal" target="_blank" rel="noopener">Prodigal</a> · <a href="https://bioinf.uni-greifswald.de/augustus/" target="_blank" rel="noopener">Augustus</a></td></tr>
    <tr><td>NCBI ORF Finder</td><td>online ORF search</td><td><a href="https://www.ncbi.nlm.nih.gov/orffinder/" target="_blank" rel="noopener">ORF Finder</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Quality control**

```bash
fastqc -o qc/ reads_R1.fastq.gz reads_R2.fastq.gz     # inspect the report
fastp -i reads_R1.fastq.gz -I reads_R2.fastq.gz \
      -o clean_R1.fastq.gz -O clean_R2.fastq.gz \
      --detect_adapter_for_pe --cut_tail --cut_mean_quality 20
```

Everything downstream depends on this. Untrimmed adapters and low-quality tails directly reduce assembly continuity.

**2. Assemble**

```bash
# small genomes such as bacteria (Illumina paired-end)
spades.py -1 clean_R1.fastq.gz -2 clean_R2.fastq.gz -o spades_out -t 8

# long reads (Nanopore / PacBio)
flye --nano-raw reads.fastq.gz --out-dir flye_out --genome-size 5m -t 8
```

> Assemblers are specialised by data type: <strong>SPAdes for short reads, Flye / Canu for long reads</strong>. Mixing them fails because the error models differ.

**3. Evaluate**

```bash
quast.py -o quast_out -R ref.fasta spades_out/scaffolds.fasta
busco -i spades_out/scaffolds.fasta -l bacteria_odb10 -m genome -o busco_out
```

**4. Predict genes**

```bash
# prokaryotes: Prodigal, simple and accurate
prodigal -i scaffolds.fasta -a proteins.faa -d genes.fna -o genes.gff -f gff

# eukaryotes: Augustus, needs a closely related species model
augustus --species=arabidopsis scaffolds.fasta > augustus.gff
```

<p>Eukaryotic genes contain introns, so species-specific trained models are essential; the wrong model misses many exons.</p>

**5. Find ORFs and translate (most intuitive at small scale)**

Paste a sequence into <a href="https://www.ncbi.nlm.nih.gov/orffinder/" target="_blank" rel="noopener">NCBI ORF Finder</a>, set the minimum ORF length and genetic code, and inspect candidate reading frames and translations. Command-line equivalents:

```bash
getorf -sequence input.fasta -outseq orfs.fasta -minsize 300 -find 3
transeq -sequence genes.fna -outseq proteins.fasta -frame 1
```

**6. Annotate**

```bash
blastp -query proteins.faa -db uniprot -evalue 1e-5 -outfmt 6 > ann.tsv
interproscan.sh -i proteins.faa -f tsv -o ipr.tsv
```

## 4. Reading the results

<ul>
  <li><strong>What N50 is</strong>: sort contigs longest first and accumulate; N50 is the length of the contig at which the cumulative total passes 50% of the assembly. It measures <strong>continuity</strong> — larger is better, but a few long contigs plus much debris can still look impressive. Always read contig count and total length alongside it.</li>
  <li><strong>BUSCO completeness</strong>: reported as Complete / Single-copy / Duplicated / Fragmented / Missing. Higher Complete is better; a high <strong>Duplicated</strong> fraction often means redundancy in the assembly (for example a heterozygous region split in two).</li>
  <li><strong>Compare with the expected genome size</strong>: far larger suggests contamination or redundancy; far smaller suggests low coverage or lost repeats.</li>
  <li><strong>Sanity-check gene counts</strong>: if the number differs from close relatives by more than a factor of two, check the model and the input.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Using an assembly without evaluating it</strong>: a high N50 does not exclude misassemblies. Read BUSCO and QUAST together.</li>
  <li><strong>Wrong prediction model</strong>: prokaryotic parameters on a eukaryote (or vice versa) generate many spurious genes.</li>
  <li><strong>Treating predictions as fact</strong>: ab initio output is a <strong>hypothesis</strong>; it needs transcript or homolog support before you rely on it.</li>
  <li><strong>Ignoring repeats</strong>: short reads always break in repeats, so contig boundaries commonly sit inside repeat families.</li>
  <li><strong>Resources</strong>: assembly is the hungriest step. Bacterial genomes run on a laptop; eukaryotic ones need a server.</li>
</ul>

## 6. Exercises

<ol>
  <li>Run fastp on a paired-end dataset and compare read counts and mean quality before and after.</li>
  <li>Assemble with SPAdes (a public small-genome dataset is fine); record contig count and N50.</li>
  <li>Run QUAST and BUSCO; report completeness percentage and fragmentation.</li>
  <li>Predict genes with Prodigal; report gene count and mean length.</li>
  <li>(Optional) Verify one predicted gene with NCBI ORF Finder and compare the start positions.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://cab.spbu.ru/software/spades/" target="_blank" rel="noopener">SPAdes manual</a></li>
  <li><a href="https://busco.ezlab.org/busco_userguide.html" target="_blank" rel="noopener">BUSCO user guide</a></li>
  <li><a href="https://www.ncbi.nlm.nih.gov/orffinder/" target="_blank" rel="noopener">NCBI ORF Finder</a></li>
  <li><a href="https://bioinf.uni-greifswald.de/augustus/" target="_blank" rel="noopener">Augustus documentation</a></li>
</ul>
