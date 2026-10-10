---
title: "Lab 15: Protein Domains, Structure Prediction and Homology Modelling"
date: "2026-10-10"
weight: 150
category: "Protein structure"
meta: "Structure · ~60 min"
module: "protein-analysis"
draft: false
summary: "Given a sequence, catalogue its domains first, then choose how to get a structure. This lab scans domains, checks transmembrane regions and signal peptides, models with SWISS-MODEL and AlphaFold, and reads the quality metrics."
---

> Module: [Protein Analysis](../posts/protein-analysis.html)

## 1. Goals

<ul>
  <li>Catalogue domains and conserved motifs with InterPro;</li>
  <li>Detect transmembrane regions and signal peptides so you do not model a membrane protein as a soluble one;</li>
  <li>Obtain structures by <strong>homology modelling</strong> and from the <strong>AlphaFold DB</strong>;</li>
  <li>Read QMEAN, Ramachandran and pLDDT, and know which regions you cannot trust.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool / database</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>InterPro</td><td>integrated domain and site scan</td><td><a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a></td></tr>
    <tr><td>Pfam / PROSITE / SMART</td><td>individual domain databases</td><td><a href="https://pfam.xfam.org/" target="_blank" rel="noopener">Pfam</a> · <a href="https://prosite.expasy.org/" target="_blank" rel="noopener">PROSITE</a> · <a href="https://smart.embl.de/" target="_blank" rel="noopener">SMART</a></td></tr>
    <tr><td>TMHMM / SignalP</td><td>transmembrane and signal peptides</td><td><a href="https://services.healthtech.dtu.dk/services/TMHMM-2.0/" target="_blank" rel="noopener">TMHMM</a> · <a href="https://services.healthtech.dtu.dk/services/SignalP-6.0/" target="_blank" rel="noopener">SignalP</a></td></tr>
    <tr><td>SWISS-MODEL</td><td>homology modelling</td><td><a href="https://swissmodel.expasy.org/" target="_blank" rel="noopener">SWISS-MODEL</a></td></tr>
    <tr><td>AlphaFold DB</td><td>predicted structure archive</td><td><a href="https://alphafold.ebi.ac.uk/" target="_blank" rel="noopener">AlphaFold DB</a></td></tr>
    <tr><td>PyMOL / ChimeraX</td><td>visualisation</td><td><a href="https://pymol.org/" target="_blank" rel="noopener">PyMOL</a> · <a href="https://www.cgl.ucsf.edu/chimerax/" target="_blank" rel="noopener">ChimeraX</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Scan for domains**

Submit the sequence to <a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a>, which merges hits from Pfam, PROSITE, SMART, CDD and others. Look for:

<ul>
  <li><strong>domain names and positions</strong> (start and end residues);</li>
  <li>annotated <strong>active-site residues</strong>;</li>
  <li>membership of a known family.</li>
</ul>

**2. Transmembrane regions and signal peptides**

Submit to <a href="https://services.healthtech.dtu.dk/services/TMHMM-2.0/" target="_blank" rel="noopener">TMHMM 2.0</a> and <a href="https://services.healthtech.dtu.dk/services/SignalP-6.0/" target="_blank" rel="noopener">SignalP 6.0</a>.

<ul>
  <li>Signal peptides sit in the first 15–30 residues and are normally <strong>removed</strong> before modelling;</li>
  <li>transmembrane helices need dedicated treatment, not a soluble-protein pipeline.</li>
</ul>

**3. Homology modelling with SWISS-MODEL**

Submit the sequence; SWISS-MODEL searches templates and reports:

<ul>
  <li>the <strong>template</strong> (PDB ID) and <strong>sequence identity</strong>;</li>
  <li>GMQE (global model quality estimate, 0–1, higher is better);</li>
  <li>QMEAN (comparison against high-quality experimental structures).</li>
</ul>

<p>Sequence identity is the lifeline of homology modelling: <strong>&gt;30% is usually usable, &gt;50% fairly reliable, below 20% the model only suggests overall topology.</strong></p>

**4. Take a predicted structure**

Check the <a href="https://alphafold.ebi.ac.uk/" target="_blank" rel="noopener">AlphaFold DB</a> first. If the protein (or a close homolog) has an entry, download the PDB together with its <strong>pLDDT confidence file</strong>.

**5. Assess quality**

<ul>
  <li><strong>pLDDT (per-residue confidence)</strong>: &gt;90 high confidence (backbone and side chains reasonably good); 70–90 backbone broadly correct; 50–70 low confidence; <strong>&lt;50 usually disordered and not a basis for conclusions</strong>.</li>
  <li><strong>Ramachandran plot</strong> (PROCHECK / MolProbity): a higher favoured-region share is better, typically &gt;98% for high quality.</li>
  <li><strong>QMEAN z-score</strong>: near 0 means comparable to experimental quality; below -4 signals trouble.</li>
</ul>

**6. Visualise**

```bash
pymol model.pdb
```

<ul>
  <li>Colour by pLDDT (standard for AlphaFold models): blue confident, orange/red not;</li>
  <li>use <code>matchmaker</code> in ChimeraX to superpose a predicted and an experimental structure and read the RMSD.</li>
</ul>

## 4. Reading the results

<ul>
  <li><strong>Domains before structure</strong>: domains hint at what it does, structure at what it looks like. Together they let you design mutations or explain phenotypes.</li>
  <li><strong>Local confidence beats global scores</strong>: a model at pLDDT 80 overall is unusable for mechanism if the active site sits in a 50-confidence stretch.</li>
  <li><strong>Predicted is not observed</strong>: AlphaFold returns one static conformation without ligands, cofactors, metals or conformational change.</li>
  <li><strong>Missing segments are normal</strong>: long insertions and disordered tails are often unmodelled; gaps in the picture are not special structural features.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Modelling a fragment</strong>: submitting only the domain loses context. Model the full length, then trim.</li>
  <li><strong>Ignoring oligomeric state</strong>: a monomer model cannot explain interface mutations; assemble the functional form when needed.</li>
  <li><strong>Building conclusions on low-confidence regions</strong>: pLDDT &lt;50 or identity &lt;20% is reference material only.</li>
  <li><strong>Not checking the template's bound state</strong>: a template from a complex may pass on a bound conformation.</li>
</ul>

## 6. Exercises

<ol>
  <li>Run InterPro on a protein of unknown function; list domains, positions and family.</li>
  <li>Use TMHMM and SignalP to decide whether it has transmembrane segments or a signal peptide.</li>
  <li>Model with SWISS-MODEL; record template PDB, identity, GMQE and QMEAN.</li>
  <li>Find the same protein in AlphaFold DB, download the PDB and colour by pLDDT in PyMOL.</li>
  <li>(Optional) Superpose the two models in ChimeraX; report RMSD and where they differ most.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a></li>
  <li><a href="https://swissmodel.expasy.org/docs/help" target="_blank" rel="noopener">SWISS-MODEL help</a></li>
  <li><a href="https://alphafold.ebi.ac.uk/faq" target="_blank" rel="noopener">AlphaFold DB FAQ (pLDDT explained)</a></li>
  <li><a href="https://www.cgl.ucsf.edu/chimerax/docs/user/index.html" target="_blank" rel="noopener">ChimeraX user guide</a></li>
</ul>
