---
title: "Multiple Sequence Alignment & Visualization"
date: "2026-10-05"
weight: 50
category: "MSA"
meta: "Sequences · ~18 min"
draft: "false"
---

<p>Pairwise alignment compares two sequences; <strong>multiple sequence alignment (MSA)</strong> stacks three or more homologs so you can spot columns conserved across species / families — these often mark functional sites or structural cores. MSA is the prerequisite for phylogenetics, protein families and motif discovery.</p>
          <h2>1. A typical workflow</h2>
          <ol>
            <li>Collect homologs: from the "Alignment &amp; BLAST" module;</li>
            <li>Deduplicate and unify to FASTA;</li>
            <li>Run MSA (MAFFT is fast and accurate);</li>
            <li>Trim low-confidence regions (trimAl);</li>
            <li>Visualize and interpret (Jalview, sequence logos).</li>
          </ol>
          <h2>2. Run MAFFT on the command line</h2>
          <pre><code># --auto picks a strategy automatically; writes aligned fasta
mafft --auto seqs.fasta &gt; aln.fasta

# parallelize for many sequences
mafft --auto --thread 8 big.fasta &gt; big_aln.fasta</code></pre>
          <p>Alternatives: ClustalOmega (stable), MUSCLE (fast). EMBL-EBI provides a no-install web MSA tool.</p>
          <h2>3. Visualize with Jalview</h2>
          <p>Jalview is the standard desktop viewer (has a Windows build):</p>
          <ul>
            <li>Open <code>aln.fasta</code> → color by conservation;</li>
            <li><strong>Conservation</strong> view highlights highly conserved columns;</li>
            <li>Compute a <strong>neighbor-joining tree</strong> for a quick cluster;</li>
            <li>Export PNG / EPS for papers.</li>
          </ul>
          <h2>4. Sequence logo: conservation as a picture</h2>
          <p>WebLogo or ggseqlogo (R) draws each column as letters whose height = frequency — taller means more conserved.</p>
          <pre><code># ggseqlogo in R
library(ggseqlogo)
p &lt;- ggseqlogo(sequences, method = "bits")
plot(p)</code></pre>
          <h2>5. How to read it</h2>
          <ul>
            <li><strong>Fully conserved columns</strong>: likely active sites or binding pockets;</li>
            <li><strong>Blocks of gaps</strong>: often flexible loops; alignment is unreliable — interpret with care;</li>
            <li><strong>Semi-conserved (e.g. K/R swap)</strong>: function kept, sequence changed.</li>
          </ul>
          <blockquote>MSA quality decides everything downstream. Forcing a distant alignment yields "false conservation". Always eyeball it after aligning — don't trust the software blindly.</blockquote>


## Mini-case

Align a few orthologs and look at conserved positions (prepare sequences yourself, or use step 3 of the Case Study):

```bash
mafft --auto tp53_orthologs.fasta > aln.fa
```

Observe: aligned sequences have equal length; open in AliView / Jalview — the `*` row marks fully conserved columns, usually key functional sites.
