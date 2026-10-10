---
title: "Common Bioinformatics Databases"
date: "2026-10-05"
weight: 30
category: "Databases"
meta: "Resources · ~15 min"
draft: "false"
---

<p>Databases are the "raw-material warehouses" of bioinformatics. This module gives you a map by data type, plus the four basic operations: query, download, submit, analyze online.</p>
          <h2>1. Map of major databases</h2>
          <table>
            <thead><tr><th>Type</th><th>Examples</th><th>Stores</th></tr></thead>
            <tbody>
              <tr><td>Sequence</td><td>NCBI, ENA, DDBJ</td><td>nucleotide / protein records</td></tr>
              <tr><td>Protein</td><td>UniProt, Pfam, InterPro</td><td>function / domain annotation</td></tr>
              <tr><td>Structure</td><td>PDB, AlphaFold DB</td><td>3D structures</td></tr>
              <tr><td>Omics</td><td>GEO, SRA, ArrayExpress</td><td>expression / raw sequencing</td></tr>
              <tr><td>Pathway</td><td>KEGG, Reactome</td><td>metabolic / signaling pathways</td></tr>
              <tr><td>Taxonomy</td><td>NCBI Taxonomy, ICTV</td><td>species / virus classification</td></tr>
              <tr><td>Literature</td><td>PubMed</td><td>paper index</td></tr>
            </tbody>
          </table>
          <h2>2. Query</h2>
          <ul>
            <li>Web search: gene name / accession (e.g. NM_00001, P12345);</li>
            <li><strong>Entrez / E-utilities</strong>: programmatic NCBI interface (for batches);</li>
            <li>Cross-db: UniProt jumps to the matching PDB / KEGG / GO in one click.</li>
          </ul>
          <h2>3. Download</h2>
          <ul>
            <li>Single: web "Send to / Download";</li>
            <li>Batch: <strong>FTP / Aspera</strong> (large files), or <code>esearch</code> + <code>efetch</code> scripts;</li>
          </ul>
          <pre><code># pull a set of nucleotides via NCBI E-utilities
esearch -db nucleotide -query "Arabidopsis[orgn]" | \
  efetch -format fasta &gt; ara.fa</code></pre>
          <h2>4. Submit and analyze online</h2>
          <ul>
            <li><strong>Submit</strong>: raw sequencing goes to SRA (need an accession); new sequences to GenBank;</li>
            <li><strong>Online analysis</strong>: many DBs ship tools — NCBI BLAST, EMBL-EBI MSA / structure prediction, UniProt BLAST and function prediction, no install needed.</li>
          </ul>
          <blockquote>When citing data, always record the <strong>accession</strong> and version. Databases update; write the version so others can reproduce your result.</blockquote>


## Mini-case

Batch-fetch a gene family's protein sequences with E-utilities:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=TP53[gene]&retmode=json"
# take the returned ids, then efetch to FASTA
```

Observe: swap `term` for any "gene[gene]" or "gene[gene]+organism" combo to batch-fetch; GEO/SRA work the same via `esearch` + `efetch`.
