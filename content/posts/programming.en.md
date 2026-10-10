---
title: "Programming Basics: R and Python"
date: "2026-10-10"
weight: 15
category: "Programming"
meta: "Basics · ~15 min"
draft: false
summary: "Real bioinformatics runs on scripts. R excels at statistics and graphics, Python at text processing and gluing pipelines together. This module tells you which to learn first and where 'good enough' lies."
---

<p>Web tools handle one or two samples, not dozens; they reproduce someone else's figure but cannot change their pipeline. At some point you will need scripts. This module helps you decide which language to start with and where you can stop.</p>

## 1. Why you cannot avoid code

<ul>
  <li><strong>Batch</strong>: QC on 30 samples or plots for 100 genes take one script run; clicking takes an afternoon.</li>
  <li><strong>Reproducibility</strong>: a script is your lab notebook. When someone asks three months later where a number came from, you re-run it.</li>
  <li><strong>Adaptability</strong>: ready-made pipelines are always slightly off. Editing other people's code is worth more than running a canned workflow.</li>
</ul>

## 2. R: statistics and figures

<p>R's role is unambiguous — <strong>differential expression, enrichment, statistical testing and publication-grade graphics</strong> live in the R ecosystem, and Bioconductor is the de facto standard for transcriptomics downstream analysis.</p>

<table>
  <thead><tr><th>Topic</th><th>What to learn</th><th>Note</th></tr></thead>
  <tbody>
    <tr><td>Data structures</td><td>vectors, data frames, factors, NA</td><td>data.frame is the daily workhorse</td></tr>
    <tr><td>Packages</td><td>CRAN, Bioconductor</td><td>omics packages come from Bioconductor and install differently</td></tr>
    <tr><td>Plotting</td><td>ggplot2 grammar (data + mapping + layers)</td><td>learn the layer mindset, not the function list</td></tr>
    <tr><td>Downstream</td><td>DESeq2 / edgeR, clusterProfiler</td><td>pairs with the RNA-seq module of this site</td></tr>
    <tr><td>Environment</td><td>RStudio (now Posit)</td><td>write, inspect and plot in one place</td></tr>
  </tbody>
</table>

## 3. Python: text processing and glue

<p>Sequences are text. <strong>Renaming records in bulk, pulling sequences by ID, parsing GenBank annotations, chaining tools into a pipeline</strong> — all are most comfortable in Python.</p>

<table>
  <thead><tr><th>Topic</th><th>What to learn</th><th>Note</th></tr></thead>
  <tbody>
    <tr><td>Core syntax</td><td>strings, lists, dicts, file I/O</td><td>dict is the core of "ID to sequence"</td></tr>
    <tr><td>Biopython</td><td>SeqIO for FASTA / GenBank</td><td>the de facto Python library for bioinformatics</td></tr>
    <tr><td>Data</td><td>pandas, numpy</td><td>tables and matrix maths</td></tr>
    <tr><td>Environment</td><td>conda / mamba, Jupyter</td><td>most omics tools ship via conda, which also tames dependencies</td></tr>
  </tbody>
</table>

## 4. Which to learn first

<table>
  <thead><tr><th>Your goal</th><th>Recommendation</th></tr></thead>
  <tbody>
    <tr><td>Differential expression, enrichment, heatmaps and volcano plots</td><td>R first; it will carry you far</td></tr>
    <tr><td>Sequence files, pipelines, data fetching</td><td>Python first</td></tr>
    <tr><td>Time for only one</td><td>R — most undergraduate downstream work happens in R</td></tr>
    <tr><td>Heading to graduate school in bioinformatics</td><td>Both: Python as the base, R for statistics</td></tr>
  </tbody>
</table>

## 5. What counts as "enough"

<ul>
  <li>You can read someone else's script and change its parameters;</li>
  <li>You can turn a repetitive action into a loop;</li>
  <li>You can read an error message, search it and build a minimal reproduction;</li>
  <li>You can tidy your own analysis into a re-runnable script.</li>
</ul>

<p>You do not need to write packages, master OOP or grind algorithm problems. <strong>Good enough is enough — learn the rest as you go.</strong></p>

## Official resources

<ul>
  <li><a href="https://www.r-project.org/" target="_blank" rel="noopener">R Project</a> · <a href="https://cran.r-project.org/" target="_blank" rel="noopener">CRAN</a> · <a href="https://www.bioconductor.org/" target="_blank" rel="noopener">Bioconductor</a></li>
  <li><a href="https://posit.co/" target="_blank" rel="noopener">Posit (formerly RStudio)</a> · <a href="https://ggplot2.tidyverse.org/" target="_blank" rel="noopener">ggplot2</a></li>
  <li><a href="https://www.python.org/" target="_blank" rel="noopener">Python</a> · <a href="https://biopython.org/" target="_blank" rel="noopener">Biopython</a></li>
  <li><a href="https://conda-forge.org/" target="_blank" rel="noopener">conda-forge</a> · <a href="https://bioconda.github.io/" target="_blank" rel="noopener">Bioconda</a> · <a href="https://jupyter.org/" target="_blank" rel="noopener">Jupyter</a></li>
</ul>
