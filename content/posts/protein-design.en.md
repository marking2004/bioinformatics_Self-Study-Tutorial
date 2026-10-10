---
title: "Peptide & Protein Design: Rational & De novo"
date: "2026-10-05"
weight: 90
category: "Design"
meta: "Proteins · ~20 min"
draft: "false"
---

<p>Analysis "reads" proteins; design "writes" them. This module covers two philosophies: editing a natural scaffold (rational design / directed evolution) and generating new scaffolds from scratch (de novo). Peptide design is the lighter, application-closer entry point (antimicrobial / binding).</p>
          <h2>1. Rational design (structure- and mechanism-based)</h2>
          <ul>
            <li><strong>Site-directed mutagenesis</strong>: change key residues to tune activity, stability or specificity (e.g. Ser→Cys to add a disulfide);</li>
            <li><strong>Consensus design</strong>: from a family MSA take the "most consensus" residues to improve thermostability;</li>
            <li><strong>Enzyme engineering</strong>: use structure + MD to estimate mutation effects.</li>
          </ul>
          <h2>2. Directed evolution ("irrational" but effective)</h2>
          <p>No structural knowledge needed: error-prone PCR introduces random mutations → library → screen / select (phage display, yeast display) → enrich over rounds. Good when the mechanism is unclear but function is needed.</p>
          <h2>3. De novo design</h2>
          <p>AI now makes "design from nothing" real, in a three-step loop:</p>
          <ol>
            <li><strong>Scaffold generation</strong>: RFdiffusion / Chroma generate new folds under constraints;</li>
            <li><strong>Sequence design</strong>: ProteinMPNN designs amino acids on a given scaffold;</li>
            <li><strong>Filter &amp; predict</strong>: re-predict with AlphaFold, keep high-pLDDT, self-consistent candidates.</li>
          </ol>
          <pre><code># RFdiffusion: generate a binder scaffold for an epitope
python run_inference.py --pmpnn True \
  --contig 'B15-25/0 0 25-35' --out_dir designs/</code></pre>
          <h2>4. Peptide-specific path</h2>
          <ul>
            <li><strong>Antimicrobial peptides (AMPs)</strong>: watch hydrophobicity, positive charge, amphipathic helix;</li>
            <li><strong>Binding / inhibitory peptides</strong>: from phage display panning, or RFdiffusion binder mode;</li>
            <li><strong>Tools</strong>: PeptideBuilder, HeliQuest, CAMPR4 (AMP DB and prediction).</li>
          </ul>
          <h2>5. A workable pipeline</h2>
          <p>Define function → pick scaffold (edit natural / generate de novo) → design sequence → <em>in silico</em> tests (folding self-consistency, docking, ADMET) → synthesis and experiment.</p>
          <blockquote>Design is "softer" than analysis: a computationally beautiful protein may not express or fold. Always prepare multiple candidates and validate in parallel — don't bet on a single sequence.</blockquote>


## Mini-case

A peek at de novo design: first predict a structure you care about with AlphaFold (download from AFDB, see step 5 of the Case Study):

```bash
curl -s "https://alphafold.ebi.ac.uk/files/AF-P04637-F1-model_v4.cif" -o P04637.cif
```

Observe: open the structure in PyMOL / ChimeraX; to actually design new proteins, move to the RFdiffusion / ProteinMPNN pipeline (needs GPU or Colab).
