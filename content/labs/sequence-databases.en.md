---
title: "Lab 4: Sequence Databases and Record Formats"
date: "2026-10-10"
weight: 40
category: "Databases"
meta: "Resources · ~40 min"
module: "databases"
draft: false
summary: "The same sequence is packaged differently in different databases. This lab reads a GenBank record field by field, separates primary from secondary databases, and teaches field-limited querying."
---

> Module: [Common Bioinformatics Databases](../posts/databases.html)

## 1. Goals

<ul>
  <li>Tell <strong>primary</strong> (raw submissions) from <strong>secondary</strong> (curated or derived) databases;</li>
  <li>Read a GenBank record field by field and know what each one answers;</li>
  <li>Write field-limited queries so the useful hit is not on page 40;</li>
  <li>Export hits as FASTA and convert between formats.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Database / tool</th><th>Type</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>NCBI GenBank</td><td>primary nucleotide</td><td><a href="https://www.ncbi.nlm.nih.gov/genbank/" target="_blank" rel="noopener">NCBI</a></td></tr>
    <tr><td>ENA (EBI)</td><td>primary nucleotide</td><td><a href="https://www.ebi.ac.uk/ena" target="_blank" rel="noopener">ENA</a></td></tr>
    <tr><td>DDBJ</td><td>primary nucleotide</td><td><a href="https://www.ddbj.nig.ac.jp/" target="_blank" rel="noopener">DDBJ</a></td></tr>
    <tr><td>UniProt</td><td>secondary protein</td><td><a href="https://www.uniprot.org/" target="_blank" rel="noopener">UniProt</a></td></tr>
    <tr><td>PDB / InterPro</td><td>structure / domains</td><td><a href="https://www.rcsb.org/" target="_blank" rel="noopener">RCSB PDB</a> · <a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a></td></tr>
    <tr><td>NGDC</td><td>national data centre</td><td><a href="https://ngdc.cncb.ac.cn/" target="_blank" rel="noopener">National Genomics Data Center</a></td></tr>
  </tbody>
</table>

<p>The three primary databases form <strong>INSDC</strong> and sync daily; the same accession works in all three — if one is slow or down, try another.</p>

## 3. Procedure

**1. Open a record and read it top to bottom**

Take any GenBank accession (for example <code>EF069996</code>). The record splits into these blocks:

<table>
  <thead><tr><th>Field</th><th>What it answers</th></tr></thead>
  <tbody>
    <tr><td>LOCUS</td><td>name, length, molecule type, submission date</td></tr>
    <tr><td>DEFINITION</td><td>one-line description of what the sequence is</td></tr>
    <tr><td>ACCESSION / VERSION</td><td>stable ID; VERSION is "accession.version", bumped when the sequence changes</td></tr>
    <tr><td>KEYWORDS / SOURCE</td><td>keywords, organism and taxonomy</td></tr>
    <tr><td>REFERENCE</td><td>related publications — a key clue to annotation reliability</td></tr>
    <tr><td>FEATURES</td><td>the annotation body: CDS, mRNA, exon, domain positions</td></tr>
    <tr><td>ORIGIN</td><td>the actual sequence, 60 bases per line with numbering</td></tr>
  </tbody>
</table>

**2. FASTA versus GenBank**

```
>EF069996.1 Oryza sativa ...        <- FASTA keeps ID + description + sequence only
ATGCGTACGG...
```

FASTA is light, fast and universally accepted, but it <strong>drops all structural annotation</strong>. For gene structure, CDS or exon work you need GenBank (or EMBL) format.

**3. Query with field limits**

Type into the NCBI search box: <code>Oryza sativa[Organism] AND NHX[Gene Name]</code>. Useful qualifiers:

<ul>
  <li><code>[Organism]</code>, <code>[Gene Name]</code>, <code>[Accession]</code>;</li>
  <li><code>[Publication Date]</code>, <code>[Sequence Length]</code>;</li>
  <li><code>AND</code> / <code>OR</code> / <code>NOT</code> to combine.</li>
</ul>

**4. Export and convert**

On a record page: <em>Send to</em> → <em>Complete Record</em> → <em>File</em> → choose FASTA or GenBank. On the command line:

```bash
seqkit seq -w 0 in.fasta > out_oneline.fasta    # one line per sequence
seqkit fx2tab in.fasta | head                    # view as a table
```

**5. Read a protein record**

Open the matching UniProt entry and focus on <em>Function</em>, <em>Family &amp; Domains</em> and <em>Sequence</em>. UniProt annotations carry <strong>evidence levels</strong>: experimental beats predicted. Distinguish them when you cite.

**6. Know your national data source**

Browse the <a href="https://ngdc.cncb.ac.cn/" target="_blank" rel="noopener">NGDC</a> and locate its genome, transcriptome and variation entries. Data from domestic projects often appear here first.

## 4. Reading the results

<ul>
  <li><strong>ACCESSION is not VERSION</strong>: cite the versioned accession (e.g. <code>EF069996.1</code>) in papers, otherwise nobody can tell which sequence revision you used.</li>
  <li><strong>RefSeq prefixes mean something</strong>: <code>NC_</code> genome, <code>NM_</code> mRNA, <code>NP_</code> protein, <code>NR_</code> non-coding RNA. These are NCBI-curated references: tidier than raw submissions, but updated more slowly.</li>
  <li><strong>CDS locations in FEATURES</strong>: <code>join(...)</code> means introns are present; <code>complement(...)</code> means the gene sits on the minus strand.</li>
  <li>The <em>Comment</em> block often states whether the sequence is complete or partial, and whether it is predicted — this directly affects what you may conclude.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Many records per gene</strong>: different cultivars and submitters produce near-identical entries. Pick your reference before any comparison.</li>
  <li><strong>Renamed organisms</strong>: after a taxonomic revision, old records keep the old name, so searching the new name misses them.</li>
  <li><strong>Predicted versus observed</strong>: annotations saying <em>by similarity</em> or <em>predicted</em> are not experimental evidence.</li>
  <li><strong>Concluding from FASTA alone</strong>: without annotations it is easy to mistake an mRNA record for a genomic one.</li>
</ul>

## 6. Exercises

<ol>
  <li>Find the nucleotide record for the <em>Arabidopsis thaliana</em> NHX gene; note accession and length.</li>
  <li>Download it in both FASTA and GenBank; compare file sizes and explain the difference.</li>
  <li>Locate the matching UniProt entry; report its length, a one-line function and its family.</li>
  <li>Write a query for "rice, submitted after 2020, longer than 1000 bp".</li>
  <li>(Optional) Find a genome relevant to your field on NGDC; record its accession and entry page.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://www.ncbi.nlm.nih.gov/genbank/samplerecord/" target="_blank" rel="noopener">GenBank sample record and field guide</a></li>
  <li><a href="https://www.insdc.org/" target="_blank" rel="noopener">INSDC official site</a></li>
  <li><a href="https://www.uniprot.org/help/text-search" target="_blank" rel="noopener">UniProt query syntax</a></li>
  <li><a href="https://seqkit.usamimi.info/" target="_blank" rel="noopener">SeqKit documentation</a></li>
</ul>
