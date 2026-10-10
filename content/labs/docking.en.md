---
title: "Lab 16: Molecular Docking and Binding-mode Analysis"
date: "2026-10-10"
weight: 160
category: "Drug design"
meta: "Drug · ~60 min"
module: "cadd"
draft: false
summary: "Docking asks whether a small molecule fits a pocket and how. This lab prepares receptor and ligand, defines the pocket, docks with Vina, analyses the binding mode, and stresses what a scoring function can and cannot tell you."
---

> Module: [Virtual Screening & CADD](../posts/cadd.html)

## 1. Goals

<ul>
  <li>Understand the two cores of docking: <strong>conformational search</strong> and <strong>scoring</strong>;</li>
  <li>Prepare a receptor (clean, protonate, define the pocket) and a ligand (3D, protonation, charges);</li>
  <li>Run a docking job with AutoDock Vina and analyse poses and key interactions;</li>
  <li>Appreciate the limits of scores and why redocking validation matters.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool / database</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>AutoDock Vina</td><td>mainstream open-source dockers</td><td><a href="https://vina.scripps.edu/" target="_blank" rel="noopener">vina.scripps.edu</a> · <a href="https://github.com/ccsb-scripps/AutoDock-Vina" target="_blank" rel="noopener">GitHub</a></td></tr>
    <tr><td>MGLTools / ADFR</td><td>receptor and ligand conversion</td><td><a href="https://ccsb.scripps.edu/mgltools/" target="_blank" rel="noopener">MGLTools</a></td></tr>
    <tr><td>CB-Dock2</td><td>online pocket prediction and docking</td><td><a href="https://cadd.labshare.cn/cb-dock2/" target="_blank" rel="noopener">CB-Dock2</a></td></tr>
    <tr><td>PubChem / ZINC</td><td>small-molecule sources</td><td><a href="https://pubchem.ncbi.nlm.nih.gov/" target="_blank" rel="noopener">PubChem</a> · <a href="https://zinc.docking.org/" target="_blank" rel="noopener">ZINC</a></td></tr>
    <tr><td>PyMOL / PLIP</td><td>visualisation and interaction analysis</td><td><a href="https://pymol.org/" target="_blank" rel="noopener">PyMOL</a> · <a href="https://plip-tool.biotec.tu-dresden.de/" target="_blank" rel="noopener">PLIP</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Prepare the receptor**

Download a structure from <a href="https://www.rcsb.org/" target="_blank" rel="noopener">RCSB PDB</a> and clean it:

<ul>
  <li>remove waters (keep any that participate in catalysis);</li>
  <li>remove the co-crystallised ligand and irrelevant chains;</li>
  <li>add hydrogens and assign charges, then save as PDBQT.</li>
</ul>

```bash
prepare_receptor4.py -r receptor.pdb -o receptor.pdbqt -A hydrogens
```

> <strong>Metal ions and cofactors</strong> are often forgotten. If the active site contains Zn²⁺, Mg²⁺ or a haem group, deleting them invalidates the docking.

**2. Prepare the ligand**

<ul>
  <li>download a 3D structure (SDF) from PubChem or ZINC;</li>
  <li>confirm the <strong>protonation state and tautomer</strong> at physiological pH;</li>
  <li>convert to PDBQT and define rotatable bonds.</li>
</ul>

```bash
obabel -isdf ligand.sdf -opdb -O ligand.pdb --gen3d
prepare_ligand4.py -l ligand.pdb -o ligand.pdbqt
```

**3. Define the docking box**

Three ways, in order of reliability:

<ol>
  <li>use the co-crystallised ligand position as the pocket centre (best);</li>
  <li>use coordinates of catalytic residues reported in the literature;</li>
  <li>predict pockets automatically with CB-Dock2 or similar.</li>
</ol>

Start with a box of 20–25 Å per side. Too small restricts conformations; too large costs accuracy and speed.

**4. Dock**

```bash
vina --receptor receptor.pdbqt --ligand ligand.pdbqt \
     --center_x 10.5 --center_y 22.0 --center_z -5.0 \
     --size_x 22 --size_y 22 --size_z 22 \
     --exhaustiveness 16 --num_modes 9 --energy_range 3 \
     --out out.pdbqt --log log.txt
```

**5. Analyse**

<ul>
  <li>read the energy ranking and whether poses converge;</li>
  <li>list hydrogen bonds, hydrophobic contacts, pi-stacking and halogen bonds with PLIP;</li>
  <li>inspect in PyMOL and check key residues against literature or mutation data.</li>
</ul>

**6. Redocking validation**

Dock the co-crystallised ligand back into its own pocket and compute the <strong>RMSD</strong> between predicted and crystal poses.

<p>RMSD below 2 Å usually means the receptor preparation and box are sound. If it is much larger, fix the setup before screening anything.</p>

## 4. Reading the results

<ul>
  <li><strong>The score ranks, it does not measure affinity</strong>. Vina returns a relative value in kcal/mol; papers often treat &lt;-7 or &lt;-8 as "looks promising", but the number <strong>is not a binding affinity</strong> and comparing scores across systems is risky.</li>
  <li><strong>Look for consistency, not the single best value</strong>: if the top three to five poses nearly coincide, confidence is higher; if each pose differs, the binding mode is undetermined.</li>
  <li><strong>Interactions need biological grounding</strong>: contacts with known catalytic or conserved residues argue more strongly than a low score alone.</li>
  <li><strong>A good score is not activity</strong>: docking is the first filter, followed by property filters and then experiments.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Dirty receptor</strong>: a leftover co-crystallised ligand occupies the pocket and pushes the new ligand elsewhere.</li>
  <li><strong>Wrong protonation</strong>: histidine forms (HID/HIE/HIP) change the hydrogen-bond network.</li>
  <li><strong>Box too large or small</strong>: too large lets ligands drift to the surface; too small restricts poses.</li>
  <li><strong>Ignoring protein flexibility</strong>: standard Vina treats the receptor as rigid; systems with strong induced fit need flexible docking or MD.</li>
  <li><strong>Using docking to explain kinetics</strong>: docking gives a static snapshot, not on- or off-rates.</li>
</ul>

## 6. Exercises

<ol>
  <li>Download a protein–ligand complex with a co-crystallised ligand; report the PDB ID and resolution.</li>
  <li>Clean and protonate the receptor; list what you removed and why.</li>
  <li>Redock the co-crystallised ligand, compute RMSD and judge whether your setup is sound.</li>
  <li>Dock a different small molecule from PubChem; report its score and main interacting residues.</li>
  <li>(Optional) Export a PLIP interaction table and compare with published key residues.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://vina.scripps.edu/manual/" target="_blank" rel="noopener">AutoDock Vina manual</a></li>
  <li><a href="https://cadd.labshare.cn/cb-dock2/" target="_blank" rel="noopener">CB-Dock2 online docking</a></li>
  <li><a href="https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index" target="_blank" rel="noopener">PLIP web server</a></li>
  <li><a href="https://www.rcsb.org/docs/general-help/ligands-in-the-pdb" target="_blank" rel="noopener">RCSB ligand guide</a></li>
</ul>
