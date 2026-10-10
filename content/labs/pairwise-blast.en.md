---
title: "Lab 6: Pairwise Alignment and BLAST Search"
date: "2026-10-10"
weight: 60
category: "Sequence analysis"
meta: "Sequences · ~50 min"
module: "sequence-alignment"
draft: false
summary: "BLAST is the most used and most misread tool in bioinformatics. This lab covers choosing the right program and database, and reading E-value, identity and coverage together."
---

> Module: [Sequence Alignment and BLAST](../posts/sequence-alignment.html)

## 1. Goals

<ul>
  <li>Distinguish <strong>global</strong> from <strong>local</strong> alignment and when each applies;</li>
  <li>Pick the right BLAST program and database for what you hold and what you seek;</li>
  <li>Run BLAST on the web and from the command line, batch it, and parse tabular output;</li>
  <li>Interpret E-value, identity and coverage correctly — avoiding traps like "70% identity means the same gene".</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>NCBI BLAST (web)</td><td>quick database search</td><td><a href="https://blast.ncbi.nlm.nih.gov/Blast.cgi" target="_blank" rel="noopener">NCBI BLAST</a></td></tr>
    <tr><td>BLAST+ CLI</td><td>batch runs, local databases</td><td><a href="https://blast.ncbi.nlm.nih.gov/doc/blast-topics/" target="_blank" rel="noopener">docs</a></td></tr>
    <tr><td>EMBOSS needle / water</td><td>pairwise global / local</td><td><a href="https://www.ebi.ac.uk/Tools/psa/" target="_blank" rel="noopener">web version</a></td></tr>
    <tr><td>UniProt / RefSeq</td><td>protein and reference databases</td><td><a href="https://www.uniprot.org/" target="_blank" rel="noopener">UniProt</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Choose the program: what do I have, what do I want**

<table>
  <thead><tr><th>Query</th><th>Database</th><th>Program</th></tr></thead>
  <tbody>
    <tr><td>nucleotide</td><td>nucleotide</td><td><code>blastn</code></td></tr>
    <tr><td>nucleotide (translated)</td><td>protein</td><td><code>blastx</code></td></tr>
    <tr><td>protein</td><td>protein</td><td><code>blastp</code></td></tr>
    <tr><td>protein</td><td>nucleotide (translated database)</td><td><code>tblastn</code></td></tr>
  </tbody>
</table>

> Key principle: <strong>protein comparisons are more sensitive than nucleotide ones for distant homologs</strong>, because the genetic code is redundant. Prefer blastp / tblastn when the relationship is remote.

**2. Web BLAST**

Open NCBI BLAST, paste the sequence, choose the program and database (<code>nr/nt</code> for everything, <code>RefSeq</code> for a curated set), optionally restrict <em>Organism</em> to cut noise, then run.

Read three blocks: <em>Graphic Summary</em> (hit distribution and scores), <em>Descriptions</em> (table) and <em>Alignments</em> (detail per hit).

**3. What each number means**

<table>
  <thead><tr><th>Metric</th><th>Meaning</th><th>How to use it</th></tr></thead>
  <tbody>
    <tr><td>Score / Bitscore</td><td>alignment quality, higher is better</td><td>compare hits for the same query</td></tr>
    <tr><td>E-value</td><td>expected number of hits this good by chance in a database this size</td><td>smaller is better; <code>1e-5</code> is a common threshold, not a law</td></tr>
    <tr><td>Percent identity</td><td>fraction of identical residues</td><td>how similar</td></tr>
    <tr><td>Query cover</td><td>fraction of the query aligned</td><td>how much — full length or just one domain</td></tr>
  </tbody>
</table>

**4. BLAST+ on the command line**

```bash
makeblastdb -in refs.fasta -dbtype nucl -out mydb

blastn -query q.fasta -db mydb \
  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" \
  -evalue 1e-5 -max_target_seqs 10 -num_threads 4 > hits.tsv

blastp -query prot.fasta -db uniprot -evalue 1e-3 -outfmt 6 > hits.tsv
```

The <code>outfmt 6</code> table opens directly in R, Python or Excel — ideal for batch runs over dozens of queries.

**5. Pairwise: global versus local**

```bash
needle -asequence a.fasta -bsequence b.fasta -gapopen 10 -gapextend 0.5 -outfile out.needle  # global
water  -asequence a.fasta -bsequence b.fasta -gapopen 10 -gapextend 0.5 -outfile out.water   # local
```

<ul>
  <li><strong>Global (Needleman-Wunsch)</strong>: aligns end to end; use for two sequences of similar length that are homologous overall.</li>
  <li><strong>Local (Smith-Waterman, the basis of BLAST)</strong>: finds the best segment; use when hunting a conserved domain inside a long sequence.</li>
</ul>

## 4. Reading the results

<ul>
  <li><strong>E-value is not similarity</strong>. It measures how likely a score this high arises by chance. Bigger database, bigger E-value for the same score, so comparing E-values across databases is meaningless.</li>
  <li><strong>Read identity and coverage together</strong>: 95% identity with 8% query cover means one short domain matched — you cannot call the whole sequences homologous.</li>
  <li><strong>Similarity is not homology; homology is not identical function</strong>. A strong hit only proves sequence similarity. Check UniProt experimental evidence; family members diverge in function.</li>
  <li><strong>The top hit can be wrong</strong>: mis-annotated entries propagate. Look at the species distribution and consistency instead of copying first place.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Wrong program</strong>: blastn against distant species often returns nothing, while blastx finds clear hits.</li>
  <li><strong>Low-complexity filtering</strong>: BLAST masks simple repeats and poly-A by default. Turn it off if those are what you are hunting.</li>
  <li><strong>nr is huge and redundant</strong>: dozens of near-identical entries inflate the table. UniProt, RefSeq or a clustered version reads far better.</li>
  <li><strong>Copying thresholds</strong>: <code>1e-5</code> is habit, not a rule. Short queries, small databases and remote searches each need their own cut-off.</li>
</ul>

## 6. Exercises

<ol>
  <li>BLAST a nucleotide sequence from your organism on the web; record the best hit's accession, identity, query cover and E-value.</li>
  <li>Rerun with blastx; compare hit counts and the best E-value, and explain the difference.</li>
  <li>Build a local database from five sequences, search it from the command line, export <code>outfmt 6</code> and sort by bitscore in a spreadsheet.</li>
  <li>Align two sequences with <code>water</code>; report the length and identity of the best local segment.</li>
  <li>(Optional) Rerun restricted to one organism and compare with the unrestricted result.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://blast.ncbi.nlm.nih.gov/doc/blast-topics/" target="_blank" rel="noopener">Official BLAST documentation</a></li>
  <li><a href="https://www.ncbi.nlm.nih.gov/books/NBK1734/" target="_blank" rel="noopener">BLAST tutorial (NCBI Bookshelf)</a></li>
  <li><a href="https://www.ebi.ac.uk/Tools/psa/" target="_blank" rel="noopener">EMBOSS pairwise alignment tools</a></li>
</ul>
