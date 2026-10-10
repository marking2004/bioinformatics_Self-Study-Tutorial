---
title: "Protein Sequence Analysis, Structure & Function"
date: "2026-10-05"
weight: 80
category: "Proteins"
meta: "Proteins · ~22 min"
draft: "false"
---

<p>From an amino-acid sequence you can read a lot: biophysical properties, structure, domains and function. This module walks the routine route from sequence to structure to function.</p>
          <h2>1. First-order properties</h2>
          <p>Use Expasy ProtParam or a local script for molecular weight, pI, instability index, half-life, hydrophobicity. For localization, check signal peptides (SignalP) and transmembrane regions (TMHMM / DeepTMHMM).</p>
          <pre><code># quick properties with Biopython
from Bio.SeqUtils.ProtParam import ProteinAnalysis
a = ProteinAnalysis("MKVLT...")
print(a.molecular_weight(), a.isoelectric_point())</code></pre>
          <h2>2. Domain and family annotation</h2>
          <ul>
            <li><strong>InterPro / Pfam</strong>: scan known domains, repeats, families;</li>
            <li><strong>CDD (NCBI)</strong>: conserved domain database;</li>
            <li><strong>PROSITE</strong>: signature motifs (e.g. active-site patterns).</li>
          </ul>
          <p>Domains tell you roughly what kind of protein it is and what it may do.</p>
          <h2>3. Structure prediction (key: AlphaFold)</h2>
          <p>Formerly homology modeling (SWISS-MODEL); today <strong>AlphaFold2 / AlphaFold3</strong> predict 3D structure from sequence at near-experimental accuracy. Easiest: search the UniProt ID in <strong>AlphaFold DB</strong> and download; locally use <strong>ColabFold</strong>.</p>
          <pre><code># local ColabFold prediction (better with GPU)
colabfold_batch seqs.fasta output_dir/</code></pre>
          <p>Two metrics: <strong>pLDDT</strong> (per-residue confidence, &gt;70 is decent) and <strong>PAE</strong> (inter-residue error; tells whether domain arrangements are trustworthy).</p>
          <h2>4. Structure visualization</h2>
          <ul>
            <li><strong>PyMOL</strong>: standard; scriptable coloring, distance, figures;</li>
            <li><strong>UCSF ChimeraX</strong>: free, friendly to large complexes;</li>
            <li><strong>Online</strong>: Mol* (PDB default viewer).</li>
          </ul>
          <h2>5. Functional annotation</h2>
          <p>Combine UniProt (function, GO terms), KEGG (pathways) and STRING (interactome) for a judgment. Automated annotation is often homology-based — confirm key claims experimentally.</p>
          <blockquote>Sequence → structure → function is a chain that gets less certain downstream. Structure prediction is accurate, but "has a structure" ≠ "known function"; be conservative about function annotation.</blockquote>


## Mini-case

Parse a protein sequence and compute its molecular weight with Biopython; annotate domains by uploading the sequence to NCBI CDD or InterPro.

```python
from Bio.Seq import Seq
from Bio.SeqUtils import molecular_weight
seq = Seq("MSK")          # replace with a real sequence
print(molecular_weight(seq, "protein"))
```

Observe: mass is in Da; domains (zinc finger, kinase, ...) usually map to specific functions and are the entry point for annotation.
