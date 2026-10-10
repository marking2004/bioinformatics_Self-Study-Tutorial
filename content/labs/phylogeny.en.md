---
title: "Lab 8: Building and Evaluating a Phylogeny"
date: "2026-10-10"
weight: 80
category: "Sequence analysis"
meta: "Sequences · ~55 min"
module: "phylogenetics"
draft: false
summary: "Between an alignment and a publishable tree sit model selection and support values. This lab runs the full route with IQ-TREE and explains branch lengths, support, and why a gene tree is not a species tree."
---

> Module: [Phylogenetics](../posts/phylogenetics.html)

## 1. Goals

<ul>
  <li>Follow the standard route: homologs → alignment → model choice → tree → support assessment;</li>
  <li>Understand <strong>distance, maximum likelihood and Bayesian</strong> approaches and when each is appropriate;</li>
  <li>Build trees with IQ-TREE and assess branches with bootstrap;</li>
  <li>Interpret branch length, support values and rooting correctly.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>IQ-TREE</td><td>ML trees with automatic model selection</td><td><a href="http://www.iqtree.org/" target="_blank" rel="noopener">iqtree.org</a> · <a href="http://iqtree.cibiv.univie.ac.at/" target="_blank" rel="noopener">web server</a></td></tr>
    <tr><td>FastTree</td><td>very fast approximate ML, good for large previews</td><td><a href="http://www.microbesonline.org/fasttree/" target="_blank" rel="noopener">FastTree</a></td></tr>
    <tr><td>MEGA</td><td>GUI, common in teaching</td><td><a href="https://www.megasoftware.net/" target="_blank" rel="noopener">MEGA</a></td></tr>
    <tr><td>FigTree / iTOL</td><td>viewing and polishing trees</td><td><a href="http://tree.bio.ed.ac.uk/software/figtree/" target="_blank" rel="noopener">FigTree</a> · <a href="https://itol.embl.de/" target="_blank" rel="noopener">iTOL</a></td></tr>
    <tr><td>ggtree (R)</td><td>programmatic tree figures</td><td><a href="https://yulab-smu.top/treedata-book/" target="_blank" rel="noopener">ggtree book</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Input: a trimmed alignment**

<p>Reuse the output of <a href="msa.html">Lab 7</a> (FASTA or PHYLIP). <strong>Alignment quality sets the ceiling on tree quality</strong> — no model rescues a bad alignment.</p>

**2. Choose a substitution model**

<p>A model states the probability of one base or residue replacing another. The wrong model biases topology and branch lengths. IQ-TREE's built-in <strong>ModelFinder</strong> compares candidates automatically:</p>

```bash
iqtree -s aligned.fasta -m TESTONLY          # model selection only
```

The <em>Best-fit model</em> line in the output is the recommendation (e.g. <code>JTT+F+I+G4</code>).

**3. Build the tree with support values**

```bash
iqtree -s aligned.fasta -m MFP -B 1000 -T 4 --prefix mytree

# quick preview for large datasets
FastTree -lg aligned.fasta > fasttree.nwk      # -lg for protein, -nt for nucleotide
```

<ul>
  <li><code>-m MFP</code>: ModelFinder Plus — select the model, then build;</li>
  <li><code>-B 1000</code>: 1000 ultrafast bootstrap replicates;</li>
  <li><code>-T 4</code>: threads.</li>
</ul>

**4. Root with an outgroup**

```bash
iqtree -s aligned.fasta -m MFP -B 1000 -o Outgroup_taxon
```

<p>Trees come out <strong>unrooted</strong> by default. To give direction you must name an outgroup known to have diverged earlier.</p>

**5. Visualise**

<ul>
  <li><strong>FigTree</strong>: open the <code>.treefile</code>, show support values, colour clades, export PDF/SVG;</li>
  <li><strong>iTOL</strong>: upload and overlay group colours, domains or heatmaps — the usual route to publication figures;</li>
  <li><strong>ggtree</strong>: scripted figures in R, best when you need many or reproducible plots.</li>
</ul>

## 4. Reading the results

<ul>
  <li><strong>Support</strong>: UFBoot ≥ 95 is generally considered reliable; classic bootstrap ≥ 70–80 is moderate. Below that, treat the branch as unresolved rather than as a finding.</li>
  <li><strong>Branch length</strong>: by default it is <strong>expected substitutions per site</strong>, not time. Statements about divergence dates require molecular-clock dating (BEAST, r8s, treePL).</li>
  <li><strong>Gene tree ≠ species tree</strong>: incomplete lineage sorting, horizontal transfer and hybridisation all make a single gene's history differ from the species'. Serious conclusions use concatenation or coalescent methods.</li>
  <li><strong>Orthologs versus paralogs</strong>: paralogs (products of gene duplication) produce a tree that looks like species relationships but records duplication events. Separate them when sampling.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Long-branch attraction</strong>: fast-evolving, long branches get pulled together erroneously. Better models (adding +G, +F) or dropping very distant taxa help.</li>
  <li><strong>Reusing one model for everything</strong>: protein and nucleotide models are not interchangeable; nucleotide models also differ in base-frequency and rate treatment.</li>
  <li><strong>Publishing NJ results</strong>: distance methods are fast but use less of the signal. Use ML or BI for final claims.</li>
  <li><strong>Mixing copies</strong>: several isoforms or paralogs from one species produce a pretty but misleading tree.</li>
  <li><strong>Reading topology without support</strong>: a tree without support values is just a picture.</li>
</ul>

## 6. Exercises

<ol>
  <li>Run <code>iqtree -m TESTONLY</code> on your Lab 7 alignment and record the best-fit model.</li>
  <li>Build with <code>-m MFP -B 1000</code> and report the share of branches with support ≥95.</li>
  <li>Rebuild with an outgroup and compare the rooted and unrooted topologies.</li>
  <li>Open the tree in FigTree, mark the least-supported branch and explain what that means biologically.</li>
  <li>(Optional) Upload to iTOL, add a group colour strip and export the figure.</li>
</ol>

## Further resources

<ul>
  <li><a href="http://www.iqtree.org/doc/" target="_blank" rel="noopener">IQ-TREE documentation</a></li>
  <li><a href="https://itol.embl.de/help.cgi" target="_blank" rel="noopener">iTOL help</a></li>
  <li><a href="https://yulab-smu.top/treedata-book/" target="_blank" rel="noopener">ggtree book</a></li>
  <li><a href="http://evolution.genetics.washington.edu/phylip/" target="_blank" rel="noopener">Phylip and phylogenetics methods</a></li>
</ul>
