---
title: "Lab 3: Python Basics and Sequence Extraction"
date: "2026-10-10"
weight: 30
category: "Programming"
meta: "Basics · ~45 min"
module: "programming"
draft: false
summary: "Sequences are text, and Python handles text well. This lab parses FASTA and GenBank with Biopython, pulls sequences by ID, computes GC content and reverse complements, and writes results in bulk."
---

> Module: [Programming Basics: R and Python](../posts/programming.html)

## 1. Goals

<ul>
  <li>Master strings, lists, dicts and file I/O in Python;</li>
  <li>Parse FASTA and GenBank with <strong>Biopython</strong>;</li>
  <li>Implement three everyday tasks: fetch by ID, GC content, reverse complement;</li>
  <li>Turn a one-off action into a re-runnable script.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>Python 3</td><td>the language</td><td><a href="https://www.python.org/" target="_blank" rel="noopener">python.org</a></td></tr>
    <tr><td>Biopython</td><td>sequence file parsing</td><td><a href="https://biopython.org/" target="_blank" rel="noopener">biopython.org</a></td></tr>
    <tr><td>conda / mamba</td><td>environments</td><td><a href="https://docs.conda.io/projects/miniconda/en/latest/" target="_blank" rel="noopener">Miniconda</a></td></tr>
    <tr><td>Jupyter</td><td>interactive work</td><td><a href="https://jupyter.org/" target="_blank" rel="noopener">jupyter.org</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Create the environment**

```bash
conda create -n pybio python=3.11 -y
conda activate pybio
conda install -c conda-forge biopython jupyter -y
```

**2. Three structures you must know**

```python
name = "AtNHX1"                      # string
seqs = ["ATGCGT", "TTACGA"]          # list
d = {"AtNHX1": "ATGCGT", "AtSOS1": "TTACGA"}   # dict: ID -> sequence
print(d[name])
for k, v in d.items():               # iterate
    print(k, len(v))
```

**3. Read and write text**

```python
with open("ids.txt") as fh:
    ids = [line.strip() for line in fh if line.strip()]
with open("out.txt", "w") as fh:
    fh.write("\n".join(ids))
```

**4. Read FASTA**

```python
from Bio import SeqIO

for rec in SeqIO.parse("seqs.fasta", "fasta"):
    print(rec.id, len(rec.seq), rec.description)
```

**5. Fetch by ID**

```python
wanted = {"AtNHX1", "AtHKT1"}
kept = [r for r in SeqIO.parse("seqs.fasta", "fasta") if r.id in wanted]
SeqIO.write(kept, "subset.fasta", "fasta")
```

**6. GC content and reverse complement**

```python
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

s = Seq("ATGCGTACGGATC")
print(f"GC: {gc_fraction(s):.2%}")
print("revcomp:", s.reverse_complement())
print("translate:", s.translate())
```

**7. Parse GenBank, list the CDS features**

```python
for rec in SeqIO.parse("record.gb", "genbank"):
    print(rec.id, rec.annotations.get("organism"))
    for feat in rec.features:
        if feat.type == "CDS":
            prod = feat.qualifiers.get("product", ["-"])[0]
            print("  CDS:", prod, feat.location)
```

**8. Tidy it into a script**

```python
#!/usr/bin/env python3
"""subset_fasta.py  extract sequences matching a list of IDs"""
import sys
from Bio import SeqIO

ids = {l.strip() for l in open(sys.argv[1]) if l.strip()}
kept = [r for r in SeqIO.parse(sys.argv[2], "fasta") if r.id in ids]
SeqIO.write(kept, sys.argv[3], "fasta")
print(f"kept {len(kept)} / wanted {len(ids)}")
```

## 4. Reading the results

<ul>
  <li>The printed <strong>kept and wanted counts should match</strong>. If kept is smaller, some IDs did not match — usually a version suffix (<code>.1</code>) or a description being treated as part of the ID.</li>
  <li>An odd GC content (say &gt;80% or &lt;20%) usually signals a problem: contamination, untrimmed adapters, or an extreme organism. Go back to the raw data.</li>
  <li>GenBank CDS features carry <code>join(...)</code> locations (eukaryotic introns). Slicing directly gives wrong results; use <code>feat.extract(rec.seq)</code>.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>ID vs description</strong>: <code>rec.id</code> is the token before the first space after <code>&gt;</code>; <code>rec.description</code> is the whole line. Match on <code>rec.id</code>.</li>
  <li><strong>Encoding</strong>: a <code>UnicodeDecodeError</code> on someone else's file usually means a non-UTF-8 encoding; try <code>encoding="utf-8"</code> or <code>errors="ignore"</code> as a stopgap.</li>
  <li><strong>Line endings</strong>: FASTA written on Windows can carry <code>\r</code>, which corrupts sequence ends on Linux.</li>
  <li><strong>Environment soup</strong>: keep one conda environment per project instead of installing everything into base.</li>
</ul>

## 6. Exercises

<ol>
  <li>Write a FASTA with five sequences and report each length and GC content with a script.</li>
  <li>Given three IDs, extract those sequences into a new file.</li>
  <li>Reverse-complement and translate one sequence; check for stop codons (<code>*</code>).</li>
  <li>Download a real GenBank record (see <a href="sequence-databases.html">Lab 4</a>) and print its organism and every CDS product name with Python.</li>
  <li>(Optional) Extend exercise 1 to process every FASTA file in a directory.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://biopython.org/wiki/Documentation" target="_blank" rel="noopener">Biopython documentation</a></li>
  <li><a href="https://biopython.org/docs/1.81/api/Bio.SeqIO.html" target="_blank" rel="noopener">SeqIO API</a></li>
  <li><a href="https://rosalind.info/problems/locations/" target="_blank" rel="noopener">Rosalind practice problems</a></li>
</ul>
