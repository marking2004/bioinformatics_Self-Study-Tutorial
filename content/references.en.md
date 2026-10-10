---
title: "References"
date: 2026-10-05
draft: false
---

A curated set of **undergraduate-friendly** bioinformatics tutorials and code projects, grouped by "English / Chinese". Most are free and open-source, and lean toward "run commands yourself". Use them as supplementary reading for this site — when you hit an unfamiliar tool or concept, come back to the relevant module here.

## English resources (command-line / genomics focused, good for starters)

- **[learn-genomics-in-linux](https://github.com/doxeylab/learn-genomics-in-linux)** (U. Waterloo): task-based command-line genomics, from Linux → BLAST → assembly → annotation → transcriptomics; the closest match to this site's spirit.
- **[Fundamentals-of-Bioinformatics](https://github.com/NIGMS/Fundamentals-of-Bioinformatics)** (Dartmouth): Bash + cloud + Conda Jupyter tutorials, including a full SRA-download → assemble-annotate-genome pipeline.
- **[genomics-workshop](https://github.com/datacarpentry/genomics-workshop)** (The Carpentries): classic genomics workshop material, great for absolute beginners.
- **[bioinformatics_tutorials](https://github.com/faylward/bioinformatics_tutorials)** (Virginia Tech): short tutorials that build on each other; do the first ~10 in order.
- **[learning-bioinformatics-at-home](https://github.com/Uzocodex/learning-bioinformatics-at-home)** (Harvard Informatics): a giant bookmark list covering Unix / R / Python / stats / RNA-seq / single-cell.
- **[DTC-Bioinformatic-Course](https://github.com/beajorrin/DTC-Bioinformatic-Course)** (WSL-based): intro course that runs bioinformatics on Windows via WSL — **especially friendly for Windows users**.
- **[Rosalind](https://rosalind.info)** (not GitHub): classic bioinformatics algorithm problem set; practice with Python/Biopython.

## Chinese resources (native-language, active communities)

- **[Bioinformatics Skills Tree — Jimmy (jmzeng1314)](https://github.com/jmzeng1314)**: one of China's most active bioinformatics communities; companion forum [bio-info-trainee.com](http://www.bio-info-trainee.com/) and a free 100-hour Bilibili video series.
- **[Xu Zhougeng (xuzhougeng)](https://github.com/xuzhougeng)**: author of *Bioinformatics for Beginners*; plain-language, quick to start.
- **[Bioinformatics Rookie Team blog](http://www.bio-info-trainee.com/)**: an evolving collection of hands-on notes from starter to advanced.

## Supplementary resources (ethnic-Chinese scholars / math & data-science foundations)

These are mostly maintained by scholars formerly at Chinese universities or ethnic-Chinese researchers; the math/DS items are especially good for filling the "prerequisites" gap of this site:

- **[bioinfomatics (xulinpan)](https://github.com/xulinpan/bioinfomatics)**: a reproducible bioinformatics tutorial built around the tumor-suppressor gene **PTEN**, combining public database records + Python pipelines + a 22-chapter LaTeX book. It threads databases → sequence → protein → domains → alignment → phylogeny → structure (AlphaFold) → variants → expression → enrichment → network → docking → MD → ML → multi-omics. Same spirit as this site's case study; great for undergrads who want one complete worked example. (Note the repo name is misspelled "bioinfomatics".)
- **[mathds (xulinpan)](https://github.com/xulinpan/mathds)**: an undergraduate *Mathematics of Data Science* textbook starter written in **R bookdown** — 12 chapters on functions/models, vectors/matrices, geometry of data, probability, inference, linear regression, classification, optimization, regularization/high-dim, dimension reduction. Fill in the math/stats foundation behind bioinformatics.
- **[dataScience (xulinpan)](https://github.com/xulinpan/dataScience)**: a machine-learning course taught at Yunnan University (Chinese), with R & Python intros, KNN, logistic regression, ggplot2, etc. Applied and beginner-friendly — a good supplement for the stats/ML side of bioinformatics.
- **[bioinfo-for-dummies (h4rvey-g)](https://github.com/h4rvey-g/bioinfo-for-dummies)**: source of the Chinese beginner book *学个毛生信* ("Learn Some Damn Bioinformatics"), written in Quarto. Zero-based, with hands-on and further-reading chapters. Native-language friendly for building intuition first.

## How to use

0. Code convention: command-line / tool steps use **bash** (language-neutral — BLAST, mafft, samtools are shell programs); **data-wrangling, plotting and stats** sections show both **R and Python** — pick either.
1. Build the big picture here first, then pick 1–2 of the projects above to go deep.
2. Stuck on the command line? Check learn-genomics-in-linux and DTC-Bioinformatic-Course first.
3. Want to practice programming? Go to Rosalind; want Chinese videos? The Skills Tree Bilibili channel.
4. Respect each project's open-source license and attribution requirements.
