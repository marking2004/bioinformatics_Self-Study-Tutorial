---
title: "Phylogenetic Analysis: Single / Multi-gene / Omics"
date: "2026-10-05"
weight: 100
category: "Phylogeny"
meta: "Evolution · ~20 min"
draft: "false"
---

<p>Phylogenetics answers "who is closer to whom". But "closer" depends on the evidence — one gene, several genes, or the whole genome. This module goes up the evidence ladder.</p>
          <h2>1. Single-gene tree (the common start)</h2>
          <p>Pipeline: MSA (see MSA module) → trim (trimAl) → pick substitution model → build → bootstrap.</p>
          <pre><code># IQ-TREE: auto model + 1000 bootstrap
iqtree2 -s aln.trim.fasta -m MFP -B 1000 -T 4</code></pre>
          <ul>
            <li><strong>Methods</strong>: neighbor-joining (fast), maximum likelihood (ML, accurate), Bayesian (slow, gives posterior);</li>
            <li><strong>Bootstrap</strong>: resampling to test node stability; &gt;70% usually trustworthy;</li>
            <li><strong>Rooting</strong>: use an outgroup to set evolutionary direction.</li>
          </ul>
          <h2>2. Multi-gene</h2>
          <p>A single gene can "lie" via incomplete lineage sorting (ILS). Two strategies:</p>
          <ul>
            <li><strong>Concatenation</strong>: stitch gene alignments into a supermatrix and build one ML tree (simple, assumes no conflict);</li>
            <li><strong>Coalescence (recommended)</strong>: build per-gene trees, then coalesce into a species tree with <strong>ASTRAL</strong> / *BEAST, handling ILS.</li>
          </ul>
          <h2>3. Omics-based</h2>
          <ul>
            <li><strong>Phylogenetic profiling</strong>: distance from gene presence/absence infers functional links;</li>
            <li><strong>Orthology matrix</strong>: OrthoFinder orthogroups → interspecies relationships;</li>
            <li><strong>SNP / variant matrix</strong>: population resequencing gives phylogenies directly (see Genomics).</li>
          </ul>
          <h2>4. Cautions when reading trees</h2>
          <blockquote>Long-branch attraction (LBA): two fast-evolving long branches get wrongly pulled together. Add outgroups, try different models, check bootstrap to expose it.</blockquote>
          <p>Branch length is amount of change; node support is trustworthiness — don't mistake a pretty tree for a correct one.</p>


## Mini-case

Build a tree from the alignment in step 4 of the Case Study; or prepare your own:

```bash
iqtree2 -s aln.fa -m MFP -bb 1000 -nt AUTO
```

Observe: `.treefile` is Newick; upload to iTOL to visualize. For multi-gene trees, concatenate several alignments and build one tree (the "multi-gene" layer).
