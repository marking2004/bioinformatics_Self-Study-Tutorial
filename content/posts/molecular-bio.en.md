---
title: "Molecular Biology: Primers, Vectors & CRISPR"
date: "2026-10-05"
weight: 20
category: "Mol. Bio"
meta: "Bench · ~18 min"
draft: "false"
---

<p>Bioinformatics serves not only computing but the bench. This module covers three "compute once before the experiment" tasks that save a lot of trial-and-error.</p>
          <h2>1. Primer design</h2>
          <ul>
            <li><strong>PCR primers</strong>: NCBI Primer-BLAST or Primer3; target Tm close (within 5℃), length 18–25 nt, GC 40–60%, product 100–500 bp;</li>
            <li><strong>Avoid</strong>: self / primer dimers, hairpins, 3′ complementarity;</li>
            <li><strong>Specificity</strong>: BLAST in the genome to confirm only the target amplifies.</li>
          </ul>
          <pre><code># Primer3 can also run on the command line (wrappers like pyPCR)
primer3_core --input input_seq.txt --output primers.txt</code></pre>
          <h2>2. Vector construction</h2>
          <ul>
            <li><strong>Restriction + ligation</strong>: classic but limited by sites;</li>
            <li><strong>Gibson / Golden Gate</strong>: seamless multi-fragment assembly; Golden Gate uses Type IIs enzymes for one-pot assembly;</li>
            <li><strong>Tools</strong>: SnapGene / Benchling for maps and primer planning (Windows builds available).</li>
          </ul>
          <h2>3. CRISPR target design and off-target</h2>
          <ol>
            <li>Pick targets: <strong>CRISPOR</strong> / <strong>CHOPCHOP</strong> find 20-nt spacers in early exons (PAM e.g. NGG);</li>
            <li>Score: on-target efficiency (e.g. CRISPOR Doench score);</li>
            <li>Off-target: <strong>Cas-OFFinder</strong> / CasFinder scan the genome for near-homologs; pick low off-target;</li>
            <li>Validate: T7E1 / Sanger or deep sequencing for editing efficiency.</li>
          </ol>
          <blockquote>On the bench, "computing" is cheap and "doing" is expensive. Primer dimers, reverse-ligated vectors, CRISPR off-targets — pitfalls avoidable in ten minutes at the computer cost a week at the bench.</blockquote>


## Mini-case

Design a pair of PCR primers: use Primer3 web (https://primer3.ut.ee/) or NCBI Primer-BLAST (https://www.ncbi.nlm.nih.gov/tools/primer-blast/); paste the target sequence to get primers and Tm.

Observe: good primers are ~18-25 nt, Tm ~55-65 C, no strong dimers/hairpins. Locally, batch-design with `primer3-py`.
