---
title: "Lab 17: Quantitative Proteomics"
date: "2026-10-10"
weight: 170
category: "Multi-omics"
meta: "Omics · ~60 min"
module: "multi-omics"
draft: false
summary: "Mass spectrometry yields spectra; a search engine turns them into proteins and quantities. This lab covers data retrieval, database search, filtering, normalisation and differential analysis — and why missing values must not be set to zero."
---

> Module: [Multi-omics Integration](../posts/multi-omics.html)

## 1. Goals

<ul>
  <li>Follow the proteomics route: digestion → LC-MS/MS → database search → quantification → statistics;</li>
  <li>Run a search with MaxQuant / FragPipe and understand FDR and enzyme settings;</li>
  <li>Distinguish <strong>DDA from DIA</strong> and <strong>labelled (TMT/iTRAQ) from label-free (LFQ)</strong> quantification;</li>
  <li>Handle missing values and select differential proteins correctly.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool / database</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>PRIDE / ProteomeXchange</td><td>public raw proteomics data</td><td><a href="https://www.ebi.ac.uk/pride/" target="_blank" rel="noopener">PRIDE</a></td></tr>
    <tr><td>MaxQuant</td><td>classic search and quantification</td><td><a href="https://www.maxquant.org/" target="_blank" rel="noopener">MaxQuant</a></td></tr>
    <tr><td>FragPipe / MSFragger</td><td>fast search, DIA support</td><td><a href="https://fragpipe.nesvilab.org/" target="_blank" rel="noopener">FragPipe</a></td></tr>
    <tr><td>Perseus</td><td>downstream statistics and plots</td><td><a href="https://www.maxquant.org/perseus/" target="_blank" rel="noopener">Perseus</a></td></tr>
    <tr><td>UniProt</td><td>protein sequence database for searching</td><td><a href="https://www.uniprot.org/" target="_blank" rel="noopener">UniProt</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Get the raw data**

Search <a href="https://www.ebi.ac.uk/pride/" target="_blank" rel="noopener">PRIDE</a>, download the raw (or converted mzML) files together with the experimental design mapping files to groups.

**2. Database search**

Key MaxQuant settings:

<ul>
  <li><strong>FASTA database</strong>: the UniProt reference proteome for the species, ideally with a common contaminant list;</li>
  <li><strong>enzyme</strong>: Trypsin/P, usually allowing 2 missed cleavages;</li>
  <li><strong>modifications</strong>: fixed carbamidomethyl on cysteine; variable methionine oxidation and N-terminal acetylation;</li>
  <li><strong>FDR</strong>: 1% at both peptide and protein level (protein-level FDR is the minimum for publication).</li>
</ul>

<p>More modifications is not better: piling on variable modifications inflates the search space and reduces identifications surviving FDR control.</p>

**3. Filter the output**

```r
dat <- dat[dat$Reverse != "+", ]                    # remove decoy hits
dat <- dat[dat$Potential.contaminant != "+", ]      # remove contaminants
dat <- dat[dat$Q.value < 0.01 & !is.na(dat$Q.value), ]
```

<ul>
  <li><strong>Reverse (decoy)</strong> and <strong>Contaminant</strong> entries (keratins, trypsin) must go;</li>
  <li>requiring at least two unique peptides per protein markedly improves reliability.</li>
</ul>

**4. Quantify and normalise**

<ul>
  <li><strong>LFQ</strong>: take MaxQuant LFQ intensities, log2 transform, then median or vsn normalisation;</li>
  <li><strong>TMT / iTRAQ</strong>: use reporter ion intensities and normalise between channels (for example IRS or median normalisation) to remove labelling and loading differences.</li>
</ul>

**5. Missing values (the crux)**

<p>Proteomics missingness is usually <strong>not random</strong>: low-abundance proteins are less likely to be detected (MNAR). Filling with zero fabricates "absent in one group". Usual practice:</p>

<ul>
  <li>filter first — keep proteins with values in at least N samples of one group;</li>
  <li>then impute with a downshifted Gaussian (Perseus), KNN or MinProb;</li>
  <li>state the imputation method and fraction in your report.</li>
</ul>

**6. Differential analysis**

```r
library(limma)
design <- model.matrix(~ 0 + group)
fit <- lmFit(log2_intensity, design)
fit <- eBayes(contrasts.fit(fit, makeContrasts(treat - ctrl, levels = design)))
topTable(fit, adjust = "BH", number = Inf)
```

## 4. Reading the results

<ul>
  <li><strong>Check identifications and FDR first</strong>: the number of proteins identified per sample should be comparable with similar published experiments. Far fewer means re-checking enzyme, modifications and database.</li>
  <li><strong>Inspect intensity boxplots</strong>: after normalisation the medians should line up; otherwise samples are not comparable.</li>
  <li><strong>Thresholds</strong>: <code>FDR &lt; 0.05 and |log2FC| &gt; 1</code> is common, though proteomics fold changes are usually smaller than transcriptomic ones, so tune to the data.</li>
  <li><strong>Transcriptome and proteome often correlate weakly</strong>: that is expected (translational regulation, degradation, sensitivity). A protein not rising when its mRNA does is not a failed experiment.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Filling missing values with zero</strong>: the classic proteomics error, which badly distorts statistics.</li>
  <li><strong>Shared peptides</strong>: when a peptide maps to several proteins, MaxQuant reports a protein group. Say you report groups, not single proteins.</li>
  <li><strong>Batch effects</strong>: MS signal drifts over time, so randomise injection order or batch will confound with group.</li>
  <li><strong>Casual modification settings</strong>: too many variable modifications wreck FDR.</li>
  <li><strong>Conflating DDA and DIA</strong>: DIA needs a spectral library or a library-free pipeline (e.g. DIA-NN); DDA parameters do not transfer.</li>
</ul>

## 6. Exercises

<ol>
  <li>Find a proteomics dataset relevant to your organism in PRIDE; record the accession and sample count.</li>
  <li>List five parameters you must set for a search and justify each.</li>
  <li>Apply the three filters to a proteinGroups.txt and report protein counts before and after.</li>
  <li>Draw boxplots before and after normalisation and say whether normalisation was needed.</li>
  <li>(Optional) Run a two-group limma analysis and compare differential counts under zero-filling versus Gaussian imputation.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://www.maxquant.org/maxquant/documentation" target="_blank" rel="noopener">MaxQuant documentation</a></li>
  <li><a href="https://fragpipe.nesvilab.org/docs/tutorial_fragpipe.html" target="_blank" rel="noopener">FragPipe tutorial</a></li>
  <li><a href="https://www.ebi.ac.uk/pride/" target="_blank" rel="noopener">PRIDE archive</a></li>
  <li><a href="https://www.uniprot.org/help/proteomes" target="_blank" rel="noopener">UniProt proteomes</a></li>
</ul>
