---
title: "Lab 13: Non-coding RNA — miRNA Discovery, Target Prediction and ceRNA Networks"
date: "2026-10-10"
weight: 130
category: "Transcriptomics"
meta: "Omics · ~60 min"
module: "rna-seq"
draft: false
summary: "miRNA calls rest on two kinds of evidence: sequence and structure. Target prediction is inherently noisy. This lab runs discovery, prediction, curated-database checking and ceRNA construction, and says which claims hold up."
---

> Module: [RNA-seq Analysis](../posts/rna-seq.html)

## 1. Goals

<ul>
  <li>Apply the two criteria for miRNA annotation: <strong>sequence homology</strong> and <strong>hairpin structure</strong>;</li>
  <li>Predict targets with mainstream web tools and understand their limits;</li>
  <li>Weight predictions using <strong>experimentally validated databases</strong>;</li>
  <li>Understand what a ceRNA network requires before it means anything.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Database / tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>miRBase</td><td>known miRNA sequences and naming</td><td><a href="https://www.mirbase.org/" target="_blank" rel="noopener">mirbase.org</a></td></tr>
    <tr><td>RNAfold (ViennaRNA)</td><td>secondary structure and MFE</td><td><a href="https://www.tbi.univie.ac.at/RNA/" target="_blank" rel="noopener">ViennaRNA</a></td></tr>
    <tr><td>psRNATarget</td><td>plant target prediction</td><td><a href="https://www.zhaolab.org/psRNATarget/" target="_blank" rel="noopener">psRNATarget</a></td></tr>
    <tr><td>TargetScan / miRanda</td><td>animal target prediction</td><td><a href="https://www.targetscan.org/" target="_blank" rel="noopener">TargetScan</a></td></tr>
    <tr><td>miRTarBase / starBase</td><td>validated targeting pairs</td><td><a href="https://mirtarbase.cuhk.edu.cn/" target="_blank" rel="noopener">miRTarBase</a> · <a href="https://starbase.sysu.edu.cn/" target="_blank" rel="noopener">starBase</a></td></tr>
    <tr><td>Cytoscape</td><td>network visualisation</td><td><a href="https://cytoscape.org/" target="_blank" rel="noopener">cytoscape.org</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Known miRNAs: homology first**

```bash
blastn -query candidates.fasta -db miRBase_mature -evalue 0.01 -outfmt 6
```

<p>Candidates identical to a known miRNA, or differing by only one or two mismatches, join that family. Note the naming: in <code>osa-miR156a</code>, <code>osa</code> is the species, <code>156</code> the family, and the trailing letter distinguishes copies.</p>

**2. Novel miRNAs: can it form a hairpin?**

```bash
RNAfold --noPS < precursor.fasta        # secondary structure and MFE
```

<p>A candidate usually needs to satisfy:</p>

<ul>
  <li>the precursor (~60–300 nt) folds into a canonical <strong>hairpin</strong>;</li>
  <li>the mature sequence sits on one arm with consistent ends (little fraying);</li>
  <li>the minimum free energy is low enough (often expressed as MFEI, MFE divided by GC content — higher is better);</li>
  <li>no large internal loops or multi-branch structures inside the hairpin.</li>
</ul>

<p>In RNAfold's dot-bracket output <code>((((...))))</code>, concentrated pairing means a tidy hairpin.</p>

**3. Target prediction**

<ul>
  <li><strong>Plants</strong>: submit to psRNATarget and read <em>Expectation</em> (lower is better) and the inhibition mode (cleavage versus translational inhibition);</li>
  <li><strong>Animals</strong>: TargetScan for seed matches and conservation; miRanda for binding free energy.</li>
</ul>

**4. Filter against curated databases**

Check predictions in <a href="https://mirtarbase.cuhk.edu.cn/" target="_blank" rel="noopener">miRTarBase</a> (experimental) or <a href="https://starbase.sysu.edu.cn/" target="_blank" rel="noopener">starBase</a> (CLIP-seq). <strong>Experimentally supported pairs far outweigh pure predictions.</strong>

**5. Build a ceRNA network**

The ceRNA hypothesis: an lncRNA or circRNA carrying the same miRNA response elements (MREs) as an mRNA competes for the miRNA and thereby modulates it. At minimum require:

<ol>
  <li>shared targeting by the same miRNA (sequence level);</li>
  <li><strong>positive correlation</strong> of expression (expression level);</li>
  <li>enough shared MREs and relative scarcity of the miRNA (dosage level).</li>
</ol>

**6. Visualise**

Assemble edge lists for "miRNA to target" and "lncRNA/circRNA to miRNA", import into Cytoscape, and distinguish the three molecule classes by shape.

## 4. Reading the results

<ul>
  <li><strong>Structure beats sequence</strong>: a sequence resembling a known miRNA that cannot fold into a hairpin does not qualify.</li>
  <li><strong>Predictions contain false positives</strong>: only a fraction of any single tool's targets survive experimental testing. Write "predicted targets" and state the tool and threshold.</li>
  <li><strong>Intersections are safer</strong>: hits from two or more tools outrank single-tool results.</li>
  <li><strong>ceRNA is a hypothesis</strong>: co-expression plus shared MREs is correlation, not regulation. Solid claims need reporter assays or knock-down experiments.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Concluding from sequence alignment alone</strong>: novel miRNAs without structural evidence rarely survive review.</li>
  <li><strong>Ignoring species-specific rules</strong>: plants mostly cleave near-perfectly complementary targets, animals act through imperfect seed pairing. The wrong model produces errors across the board.</li>
  <li><strong>Calling predictions validation</strong>: a "target gene" backed only by prediction is far weaker than one backed by a dual-luciferase assay.</li>
  <li><strong>Over-reading ceRNA networks</strong>: presenting a hundred-node diagram as a demonstrated mechanism is the classic flaw of this analysis.</li>
</ul>

## 6. Exercises

<ol>
  <li>Download known mature miRNA sequences for your organism from miRBase; count families.</li>
  <li>Fold one candidate precursor with RNAfold; draw the hairpin and report the MFE.</li>
  <li>Predict targets with psRNATarget or TargetScan; record tool, parameters and hit count.</li>
  <li>Check two of those pairs in miRTarBase or starBase for experimental support.</li>
  <li>(Optional) Build a small ceRNA network, plot it in Cytoscape and state your filters.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://www.mirbase.org/help/nomenclature.shtml" target="_blank" rel="noopener">miRNA nomenclature</a></li>
  <li><a href="https://www.tbi.univie.ac.at/RNA/RNAfold.1.html" target="_blank" rel="noopener">RNAfold manual</a></li>
  <li><a href="https://www.zhaolab.org/psRNATarget/" target="_blank" rel="noopener">psRNATarget</a></li>
  <li><a href="https://mirtarbase.cuhk.edu.cn/" target="_blank" rel="noopener">miRTarBase</a></li>
</ul>
