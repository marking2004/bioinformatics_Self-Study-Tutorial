---
title: "Alignment & BLAST: Find Homologs from One Sequence"
date: "2026-10-05"
weight: 40
category: "Sequences"
meta: "Sequences · ~12 min"
draft: "false"
---

<p>Alignment is the "grammar" of bioinformatics. With an unknown sequence, the first question is usually: who does it look like? That is exactly what BLAST does.</p>
          <h2>1. Why align</h2>
          <p>Two sequences being "similar" usually means shared ancestry or function. Alignment stacks them and marks matching vs. mutated positions — the basis for almost all downstream interpretation.</p>
          <h2>2. How BLAST works (intuition)</h2>
          <p>BLAST does not brute-force all sequences (too slow). It first finds short highly-similar "seeds", then extends them. That is why it is fast and accurate enough for most tasks.</p>
          <ul>
            <li>Input your query sequence;</li>
            <li>Find short, highly similar seed hits in the database;</li>
            <li>Extend seeds into local alignments;</li>
            <li>Use the E-value to judge significance (smaller = more trustworthy).</li>
          </ul>
          <h2>3. Run BLAST on the command line</h2>
          <pre><code># align query.fa against the nt database with local blastn
blastn -query query.fa -db nt -out result.tsv \
       -outfmt 6 -evalue 1e-5 -num_threads 4</code></pre>
          <p><code>-outfmt 6</code> gives a tab-separated table you can pipe into the <code>cut</code> / <code>sort</code> commands from the previous lesson.</p>
          <h2>4. Reading the result: E-value and bit score</h2>
          <table>
            <thead><tr><th>Field</th><th>Meaning</th></tr></thead>
            <tbody>
              <tr><td>E value</td><td>probability of a random match this good; smaller = more reliable</td></tr>
              <tr><td>Bitscore</td><td>alignment score; larger = more similar</td></tr>
              <tr><td>% identity</td><td>percent identity</td></tr>
            </tbody>
          </table>
          <p>Do not trust high identity alone: two very short sequences at 100% may still be unreliable — always check the E-value.</p>
          <h2>5. Pairwise vs. database search</h2>
          <p>Searching one sequence against a database (e.g. NCBI blastn) is a <strong>database search</strong>; aligning two sequences directly (Needleman-Wunsch global, Smith-Waterman local) is a <strong>pairwise alignment</strong>, used for fine comparison.</p>
          <blockquote>Alignment balances mismatches against gaps; the gap penalty decides what the final alignment looks like.</blockquote>


## Mini-case

Align two DNA sequences with nucleotide blastn (build the database first):

```bash
makeblastdb -in subject.fa -dbtype nucl
blastn -query query.fa -db subject.fa -outfmt 6
```

Observe: the last column `evalue` — smaller is more significant; identity is in `pident`. Try NCBI web BLAST first, then batch on the command line.
