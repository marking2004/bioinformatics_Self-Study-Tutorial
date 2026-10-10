---
title: "Virtual Screening & Computer-aided Drug Design"
date: "2026-10-05"
weight: 120
category: "Drug Design"
meta: "Drug · ~20 min"
draft: "false"
---

<p>Computer-aided drug design (CADD) uses structure and computation to pick a few "worth synthesizing" candidates from a huge chemical space. This module follows a standard chain: target → docking → screening → property check.</p>
          <h2>1. Prepare the target structure</h2>
          <ul>
            <li>Get the protein from PDB / AlphaFold DB, strip water, add hydrogens, fix side chains (PyMOL / ChimeraX);</li>
            <li>Define the <strong>binding pocket</strong>: known ligand position, homologous structure, or SiteMap / fpocket prediction.</li>
          </ul>
          <h2>2. Molecular docking (core)</h2>
          <p>Fit small molecules into the pocket and score binding. <strong>AutoDock Vina</strong> is free and fast:</p>
          <pre><code># prepare receptor/ligand as pdbqt, then dock
vina --receptor rec.pdbqt --ligand lig.pdbqt \
     --config box.txt --out out.pdbqt</code></pre>
          <p>Docking scores are relative rankings, not absolute affinities; different tools on the same protein may disagree — cross-validate.</p>
          <h2>3. Virtual screening</h2>
          <p>Batch-dock a large library (ZINC, PubChem, Enamine), keep top scores. Tip: filter for drug-likeness and deduplicate the library before screening to save time.</p>
          <h2>4. ADMET and drug-likeness</h2>
          <p>Good binding ≠ druggable. Use <strong>SwissADME</strong> / admetSAR:</p>
          <ul>
            <li><strong>Lipinski's rule of five</strong>: MW, logP, H-bond donors/acceptors;</li>
            <li><strong>ADMET</strong>: absorption, distribution, metabolism, excretion, toxicity;</li>
            <li><strong>Aqueous solubility / permeability</strong>: e.g. ALOGPS, SwissADME solubility estimates, relevant to oral absorption;</li>
            <li><strong>Skin sensitization</strong>: e.g. OECD QSAR Toolbox, admetSAR sensitization models, for contact-risk assessment;</li>
            <li><strong>Toxicity / off-target</strong>: hERG, CYP inhibition, etc.</li>
          </ul>
          <h2>5. Ligand structure generation &amp; optimization</h2>
          <p>Once you have a ligand (a SMILES, or downloaded from ZINC / PubChem), turn it into a "dockable 3D structure":</p>
          <ul>
            <li><strong>2D → 3D</strong>: generate an initial 3D conformation with Open Babel (<code>obabel mol.smi -O mol.pdb --gen3d</code>) or RDKit;</li>
            <li><strong>Conformer search / force-field optimization</strong>: MMFF94 (Open Babel / RDKit), UFF — pick a low-energy conformer as docking input;</li>
            <li><strong>Protonation / tautomers</strong>: cxcalc, Open Babel (<code>--p</code>) or ChemAxon for the dominant form at a given pH;</li>
            <li><strong>Dedup &amp; drug-likeness prefilter</strong>: keep one low-energy conformer per molecule, filter by Lipinski / PAINS before docking.</li>
          </ul>
          <p>A few molecules can be drawn by hand (MarvinSketch, ChemDraw) then converted to 3D; batch generation uses RDKit scripts. This step decides whether the conformer fed to docking is reasonable, and directly affects scores.</p>
          <h2>6. Lead optimization</h2>
          <p>With a hit, use structure to modify substituents, tune pK and selectivity, cycling "design — synthesize — test". Generative models (e.g. REINVENT) now explore chemical space.</p>
          <blockquote>Docking is a filter, not a predictor. Top candidates still need wet validation (SPR / enzymatic / cellular); don't read a docking score as an IC50.</blockquote>


## Mini-case

Docking primer: use SwissDock web (http://www.swissdock.ch/) to upload a protein PDB and a ligand for binding-pocket scores; locally use AutoDock Vina:

```bash
conda install -c bioconda autodock-vina
vina --receptor receptor.pdbqt --ligand ligand.pdbqt --out out.pdbqt --exhaustiveness 8
```

Observe: results are ranked by binding free energy — more negative is better. For deeper design see the peptide/protein design module.
