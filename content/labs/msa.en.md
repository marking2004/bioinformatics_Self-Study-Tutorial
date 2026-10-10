---
title: "Lab 7: Multiple Sequence Alignment and Visualisation"
date: "2026-10-10"
weight: 70
category: "Sequence analysis"
meta: "Sequences · ~50 min"
module: "msa"
draft: false
summary: "Stacking homologs reveals which positions evolution kept. This lab aligns with MAFFT, dereplicates, trims and visualises an alignment, then judges whether the result can be trusted."
---

> Module: [Multiple Sequence Alignment & Visualisation](../posts/msa.html)

## 1. Goals

<ul>
  <li>Understand why we do MSA: to find the <strong>conserved columns</strong> across species or families;</li>
  <li>Align online and from the command line, and know where MAFFT / MUSCLE / Clustal Omega each fit;</li>
  <li>Complete the full route: <strong>dereplicate, trim, visualise</strong>;</li>
  <li>Judge whether an alignment is good enough for tree building or functional-site work.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>MAFFT</td><td>mainstream aligner, fast and accurate</td><td><a href="https://mafft.cbrc.jp/alignment/software/" target="_blank" rel="noopener">software</a> · <a href="https://mafft.cbrc.jp/alignment/server/" target="_blank" rel="noopener">server</a></td></tr>
    <tr><td>MUSCLE / Clustal Omega</td><td>alternatives</td><td><a href="https://www.ebi.ac.uk/Tools/msa/" target="_blank" rel="noopener">EBI web</a></td></tr>
    <tr><td>trimAl</td><td>trim unreliable regions</td><td><a href="http://trimal.cgenomics.org/" target="_blank" rel="noopener">trimal</a></td></tr>
    <tr><td>Jalview</td><td>view and edit alignments locally</td><td><a href="https://www.jalview.org/" target="_blank" rel="noopener">jalview.org</a></td></tr>
    <tr><td>WebLogo / ESPript</td><td>conservation graphics</td><td><a href="https://weblogo.berkeley.edu/" target="_blank" rel="noopener">WebLogo</a> · <a href="https://espript.ibcp.fr/" target="_blank" rel="noopener">ESPript</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Prepare input: homologous, not over-redundant**

<p>MSA assumes <strong>homology</strong>. Input usually comes from BLAST top hits, but check:</p>

<ul>
  <li>drop near-identical duplicates (redundancy biases the alignment toward large families);</li>
  <li>make sure all sequences run in the same direction — reverse-complement the odd ones;</li>
  <li>10–50 sequences is a good range: too few makes conservation unreliable, too many hurts alignment quality.</li>
</ul>

```bash
seqkit seq -r -p seqs.fasta > rc.fasta          # reverse complement if needed
seqkit rmdup -s seqs.fasta > dedup.fasta        # dereplicate by sequence
seqkit stats dedup.fasta
```

**2. Online alignment (fastest for a few sequences)**

Paste FASTA into the <a href="https://mafft.cbrc.jp/alignment/server/" target="_blank" rel="noopener">MAFFT server</a>, keep the default strategy (<code>--auto</code>), and open the result in Jalview.

**3. Command-line alignment**

```bash
mafft --auto --thread 4 input.fasta > aligned.fasta
muscle -align input.fasta -output aligned.fasta          # alternative
```

Useful flags: <code>--maxiterate 1000 --localpair</code> (accuracy first, for few sequences), <code>--auto</code> (balanced), <code>--thread</code> (parallel).

**4. Trim unreliable regions**

```bash
trimal -in aligned.fasta -out trimmed.fasta -automated1
```

Gap-rich or locally messy regions distort trees, so trimming is usually wise — but keep the full length when you need to display functional sites in context.

**5. Visualise conservation**

<ul>
  <li><strong>Jalview</strong>: colour columns by hydrophobicity or conservation; fully conserved columns stand out.</li>
  <li><strong>WebLogo</strong>: letter height encodes information content; tall positions are conserved.</li>
  <li><strong>ESPript</strong>: publication-quality figures, able to overlay secondary structure.</li>
</ul>

**6. Convert for downstream tools**

```bash
seqkit convert --to phylip aligned.fasta > aligned.phy   # for tree programs
```

## 4. Reading the results

<ul>
  <li><strong>Look at column identity</strong>: columns identical across all sequences often mark functional sites or structural cores — prime targets for mutagenesis.</li>
  <li><strong>Look at gap distribution</strong>: gaps clustered in the same region of a few sequences suggest an insertion, or that the region is not homologous at all.</li>
  <li><strong>Look at the ends</strong>: ragged ends are normal because sequences differ in length. If the middle is also badly staggered, the input is probably not homologous.</li>
  <li><strong>Self-check</strong>: align with two different programs. If the conserved columns agree, the alignment is trustworthy.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Including non-homologous sequences</strong>: MSA aligns mechanically; it never judges homology. The result looks plausible and the conclusion is wrong.</li>
  <li><strong>Mixed orientations</strong>: one reversed sequence wrecks the alignment. Check or normalise direction first.</li>
  <li><strong>Trusting defaults for distant sequences</strong>: switch to <code>--localpair --maxiterate</code> for remote homologs.</li>
  <li><strong>Building trees on untrimmed alignments</strong>: programs treat gaps differently; trimming first is safer.</li>
</ul>

## 6. Exercises

<ol>
  <li>Collect 10–20 homologous protein sequences for a gene family via BLAST and state your filters.</li>
  <li>Align with MAFFT; report alignment length and the number of fully conserved columns.</li>
  <li>Trim with trimAl and compare lengths before and after.</li>
  <li>Open in Jalview, mark the sites you consider functionally conserved and justify them.</li>
  <li>(Optional) Submit to WebLogo, capture the conservation plot and identify the position with the highest information content.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://mafft.cbrc.jp/alignment/software/" target="_blank" rel="noopener">MAFFT documentation</a></li>
  <li><a href="https://www.jalview.org/help/html/features.html" target="_blank" rel="noopener">Jalview features</a></li>
  <li><a href="http://trimal.cgenomics.org/" target="_blank" rel="noopener">trimAl usage</a></li>
</ul>
