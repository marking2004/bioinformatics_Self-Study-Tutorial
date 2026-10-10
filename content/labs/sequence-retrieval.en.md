---
title: "Lab 5: Retrieving Sequences and Raw Reads"
date: "2026-10-10"
weight: 50
category: "Databases"
meta: "Resources · ~45 min"
module: "databases"
draft: false
summary: "Data can be clicked or pulled. This lab does both: batch sequence retrieval with E-utilities, raw read download with the SRA Toolkit, alternative sourcing from ENA/DDBJ, and integrity checks."
---

> Module: [Common Bioinformatics Databases](../posts/databases.html)

## 1. Goals

<ul>
  <li>Know both retrieval routes — web and command line — and when each fits;</li>
  <li>Fetch sequences in bulk with <strong>Entrez Direct (E-utilities)</strong>;</li>
  <li>Download raw sequencing data with the <strong>SRA Toolkit</strong>;</li>
  <li>Verify downloads (counts, line numbers, md5) so a half-missing file never reaches your pipeline.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool / interface</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>Entrez Direct</td><td>NCBI command-line search and fetch</td><td><a href="https://www.ncbi.nlm.nih.gov/books/NBK179288/" target="_blank" rel="noopener">manual</a></td></tr>
    <tr><td>SRA Toolkit</td><td>raw read download and conversion</td><td><a href="https://github.com/ncbi/sra-tools" target="_blank" rel="noopener">GitHub</a></td></tr>
    <tr><td>ENA Browser API</td><td>EBI-side download</td><td><a href="https://www.ebi.ac.uk/ena/browser/api/" target="_blank" rel="noopener">API docs</a></td></tr>
    <tr><td>DDBJ</td><td>Japanese mirror entry point</td><td><a href="https://www.ddbj.nig.ac.jp/" target="_blank" rel="noopener">DDBJ</a></td></tr>
    <tr><td>Ensembl REST / BioMart</td><td>genome-scale retrieval</td><td><a href="https://rest.ensembl.org/" target="_blank" rel="noopener">REST</a> · <a href="https://www.ensembl.org/biomart/martview" target="_blank" rel="noopener">BioMart</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Web route: one or a few records**

Record page → <em>Send to</em> → <em>File</em> → pick a format. Fine for a handful; past a few dozen, switch to the command line.

**2. Command line: E-utilities**

```bash
esearch -db nuccore -query "Oryza sativa[Organism] AND NHX[Gene Name]" > esearch.xml
efetch -db nuccore -format fasta -input esearch.xml > nhx.fasta

# in one pipe
esearch -db nuccore -query "Oryza sativa[Organism] AND NHX[Gene Name]" \
  | efetch -format fasta > nhx.fasta

grep -c ">" nhx.fasta     # how many did we get
```

Useful flags: <code>-db</code> (nuccore / protein / sra / pubmed), <code>-format</code> (fasta / genbank), <code>-id</code> for an accession list.

**3. Raw reads from SRA**

```bash
prefetch SRR12345678                              # download the .sra package
fasterq-dump SRR12345678 --split-files --gzip     # to FASTQ, paired-end split into R1/R2
```

The same run is often faster straight from ENA as FASTQ:

```bash
curl -L "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRR12345678&result=read_run&fields=fastq_ftp"
# prefix the returned FTP path with http and download it
```

**4. A genome region from Ensembl**

```bash
curl "https://rest.ensembl.org/sequence/region/human/1:1000000-1000500:1?content-type=text/plain"
```

For a gene list, BioMart's web interface with exported attributes beats writing API calls.

**5. Verify**

```bash
seqkit stats nhx.fasta                 # count and lengths
wc -l reads.fastq                      # FASTQ lines = reads x 4
md5sum reads.fastq.gz                  # compare with the source md5
```

## 4. Reading the results

<ul>
  <li><strong>FASTQ lines = reads x 4</strong>. If it does not divide evenly, the file is truncated or mis-joined — download again.</li>
  <li><strong>Paired files must match</strong>: R1 and R2 have identical read counts in the same order. If not, they cannot go into an aligner as-is.</li>
  <li>The <code>Count</code> from <code>esearch</code> should match what <code>efetch</code> returns; a big gap usually means temporary or restricted records.</li>
  <li>An interrupted download leaves a file that exists but is incomplete. <strong>Verified means obtained.</strong></li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>NCBI rate limits</strong>: without an API key you get roughly 3 requests per second. Use a key, or <code>sleep</code> in the loop, or your IP gets blocked.</li>
  <li><strong>Disk space</strong>: one SRA run is often several GB and larger unpacked. Check <code>df -h</code> first.</li>
  <li><strong>SRA Toolkit versions</strong>: older builds cannot read newer formats. Install via conda and keep it current.</li>
  <li><strong>Broken transfers</strong>: use <code>wget -c</code> (resume) or <code>aria2c</code> for big files, not a browser dialog.</li>
  <li><strong>Genome build mismatch</strong>: Ensembl and NCBI version their genomes differently; mixing them breaks coordinates.</li>
</ul>

## 6. Exercises

<ol>
  <li>Search a gene family in an organism you know with <code>esearch</code>; record the query and hit count.</li>
  <li>Export to FASTA and report count, shortest and longest length with <code>seqkit stats</code>.</li>
  <li>Download a public single-end SRA run and confirm the FASTQ line count divides by 4.</li>
  <li>Look up the same accession through the ENA API and compare download speeds.</li>
  <li>(Optional) Write a shell loop that downloads from an accession list and verifies each file automatically.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://www.ncbi.nlm.nih.gov/books/NBK179288/" target="_blank" rel="noopener">Entrez Direct manual</a></li>
  <li><a href="https://github.com/ncbi/sra-tools/wiki/HowTo:-fasterq-dump" target="_blank" rel="noopener">fasterq-dump how-to</a></li>
  <li><a href="https://www.ebi.ac.uk/ena/browser/api/" target="_blank" rel="noopener">ENA Browser API</a></li>
  <li><a href="https://rest.ensembl.org/documentation" target="_blank" rel="noopener">Ensembl REST documentation</a></li>
</ul>
