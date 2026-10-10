---
title: "Lab 10: Genome Visualisation and Browser Work"
date: "2026-10-10"
weight: 100
category: "Genomics"
meta: "Omics · ~45 min"
module: "genomics"
draft: false
summary: "Genomic data only makes sense on coordinates. This lab uses Ensembl, UCSC and local IGV to inspect gene structure, coverage and variants, and nails down coordinates and genome versions."
---

> Module: [Nucleic-acid Analysis & Genomics](../posts/genomics.html)

## 1. Goals

<ul>
  <li>Understand the browser design: a coordinate axis with tracks as layers;</li>
  <li>Find transcripts, exons and homologs in Ensembl, UCSC and NCBI;</li>
  <li>Inspect alignments and coverage peaks locally with <strong>IGV</strong>;</li>
  <li>Get the coordinate conventions of custom tracks (BED / GFF) right.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>Ensembl</td><td>gene structure and annotation</td><td><a href="https://www.ensembl.org/" target="_blank" rel="noopener">ensembl.org</a></td></tr>
    <tr><td>UCSC Genome Browser</td><td>multi-track overlay, BLAT</td><td><a href="https://genome.ucsc.edu/" target="_blank" rel="noopener">genome.ucsc.edu</a></td></tr>
    <tr><td>NCBI Genome Data Viewer</td><td>NCBI's genome view</td><td><a href="https://www.ncbi.nlm.nih.gov/gdv/" target="_blank" rel="noopener">GDV</a></td></tr>
    <tr><td>IGV</td><td>local alignment and variant viewing</td><td><a href="https://igv.org/" target="_blank" rel="noopener">igv.org</a></td></tr>
    <tr><td>JBrowse 2</td><td>self-hosted web browser</td><td><a href="https://jbrowse2.jbrowse.org/" target="_blank" rel="noopener">JBrowse 2</a></td></tr>
    <tr><td>samtools</td><td>sorting and indexing alignments</td><td><a href="https://www.htslib.org/" target="_blank" rel="noopener">htslib</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Fix the genome build first**

<p>Confirm which assembly you are on (for human, <code>GRCh38/hg38</code> versus <code>GRCh37/hg19</code>). <strong>Coordinates do not transfer between builds</strong> — this is the most common cause of rework.</p>

**2. Read a gene in Ensembl**

Search the gene name and open the Gene page. Focus on:
<ul>
  <li><em>Transcripts</em>: one gene often has several isoforms; only the one marked <em>canonical</em> is the default;</li>
  <li>the transcript diagram: filled blocks are exons (thicker for CDS, thinner for UTR), thin lines are introns;</li>
  <li>direction: an arrow pointing left means the gene is on the minus strand, so the sequence must be reverse-complemented.</li>
</ul>

**3. Overlay tracks in UCSC**

After navigating to a region, tick the tracks you need (<em>RefSeq Genes</em>, <em>dbSNP</em>, <em>Conservation</em>). <em>BLAT</em> maps a sequence back onto the genome quickly.

**4. Local data in IGV**

```bash
samtools faidx ref.fasta                    # index the reference
samtools sort -@ 4 -o sorted.bam aln.sam    # SAM to sorted BAM
samtools index sorted.bam                   # build .bai (required by IGV)
```

In IGV: <em>Genomes → Load Genome from File</em> for <code>ref.fasta</code>, then <em>File → Load from File</em> for <code>sorted.bam</code> and <code>genes.gff</code>.

**5. Custom tracks**

<ul>
  <li><strong>BED</strong>: 0-based, half-open, three required columns (chrom, start, end);</li>
  <li><strong>GFF / GTF</strong>: 1-based, closed interval, attributes in column 9.</li>
</ul>

```bash
samtools view -h sorted.bam chr1:1000000-1001000 | head
```

## 4. Reading the results

<ul>
  <li><strong>Coverage peaks</strong>: the grey histogram at the top is depth. Continuous high coverage across an exon means high expression; peaks on only some exons suggest isoform differences or degradation.</li>
  <li><strong>Junction reads</strong>: a read with a gap (N, or a line skipping a region) crosses a splice site — direct evidence of a transcript.</li>
  <li><strong>Variants</strong>: coloured bars mark bases differing from the reference. Roughly 50/50 colour proportions indicate heterozygosity, near 100% homozygosity; below 20%, suspect sequencing error.</li>
  <li><strong>Strand</strong>: the arrow direction decides whether you reverse-complement when extracting sequence or designing primers.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Off-by-one coordinates</strong>: BED is 0-based half-open, GFF is 1-based closed. Forgetting the shift when converting moves your interval by one base — potentially fatal in cloning.</li>
  <li><strong>Mixing builds</strong>: hg19 coordinates viewed on hg38 land somewhere else entirely. Use LiftOver to convert.</li>
  <li><strong>Unindexed BAM</strong>: IGV cannot seek, so loading fails or crawls. Always <code>samtools index</code>.</li>
  <li><strong>Oversized files</strong>: convert genome-wide coverage to BigWig before loading; dragging a raw BAM onto a large genome stalls the program.</li>
  <li><strong>Assuming the default transcript</strong>: a gene may have a dozen isoforms. State which one your conclusion depends on.</li>
</ul>

## 6. Exercises

<ol>
  <li>Find a familiar gene in Ensembl; record its ID, location, strand and transcript count.</li>
  <li>Extract one exon's sequence and locate it with UCSC BLAT; confirm the coordinates match.</li>
  <li>Index an alignment with samtools, load it in IGV, screenshot it and mark a coverage peak.</li>
  <li>Write a three-line BED file by hand, load it, and verify the displayed position matches your intent.</li>
  <li>(Optional) Compare the transcript count for the same gene in Ensembl and NCBI GDV and explain any difference.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://igv.org/doc/desktop/" target="_blank" rel="noopener">IGV desktop documentation</a></li>
  <li><a href="https://genome.ucsc.edu/goldenPath/help/hgTracksHelp.html" target="_blank" rel="noopener">UCSC browser help</a></li>
  <li><a href="https://www.ensembl.org/info/website/tutorials/index.html" target="_blank" rel="noopener">Ensembl tutorials</a></li>
  <li><a href="https://www.htslib.org/doc/samtools.html" target="_blank" rel="noopener">samtools documentation</a></li>
</ul>
