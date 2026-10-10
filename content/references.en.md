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

## Textbooks & bibliography

### Print textbooks (listed only — no electronic copies offered)

All titles below are **in-print commercial publications**. This site only provides bibliographic records and **does not host or link to PDFs or scans** — please obtain them via a library, the publisher, or a legitimate bookshop. The first two titles are the reference framework behind this site's lab exercises.

| Title | Author / Editor | Publisher | Year | ISBN |
|---|---|---|---|---|
| 生物信息学实验指导 (Bioinformatics Lab Manual) | Fan Longjiang, Ye Chuyu (eds.) | Science Press (科学出版社) | 2022 | 978-7-03-072304-8 |
| 生物信息学实验 (Bioinformatics Experiments) | Chen Ming, Yuan Chunhui (eds.) | Science Press (科学出版社) | 2022 | 978-7-03-071689-7 |
| 生物信息学 (Bioinformatics, 2nd ed.) | Fan Longjiang (ed.) | Science Press (科学出版社) | 2021 | 9787030681010 |
| 生物信息学 (Bioinformatics, 4th ed.) | Chen Ming (ed.) | Science Press (科学出版社) | — | — |
| 生物信息学 (Bioinformatics, "101 Plan" core textbook) | Chen Ming, Lü Hui (eds.) | — | — | — |
| 生物信息学分析实践 (Bioinformatics Analysis in Practice) | Wu Zujian et al. | — | — | — |
| 生物信息学 (Bioinformatics) | Wang Jingjing, Cai He | Tsinghua University Press | 2014 | 978-7-302-36241-8 |
| 生物信息学导论——面向高性能计算的算法与应用 (Introduction to Bioinformatics: Algorithms and Applications for High-Performance Computing) | Wang Yongxian, Wang Zhenghua | Tsinghua University Press | 2011 | 978-7-302-25022-7 |
| 分子进化与系统发育 (Molecular Evolution and Phylogenetics) | M. Nei, S. Kumar | — | — | — |
| 轻松构建系统发育树：实用操作方法和理论 (Phylogenetic Trees Made Easy, 4th ed.) | B. G. Hall; trans. Chen Shichao, Fu Chengxin, Wu Xiaoyun | — | — | — |

A dash "—" means no reliable source was verified for that field; it is left blank rather than guessed. Companion teaching materials for *Bioinformatics* (2nd ed., Fan Longjiang) are published by the editor's lab on its group homepage (ibi.zju.edu.cn/bioinplant).

### Open-access online textbooks and courses (start reading now)

Compared with print books, these are updated more often and free to read online — good immediate companions to this site:

- **[Galaxy Training Network](https://training.galaxyproject.org/)**: official Galaxy training network, topic-organised tutorials (some translated into Chinese), from beginner to advanced, all runnable online.
- **[EMBL-EBI training](https://www.ebi.ac.uk/training/)**: online courses and tutorial library from the European Bioinformatics Institute — sequence analysis, structure, omics; consistently high quality.
- **[Bioinformatics Algorithms](https://www.bioinformaticsalgorithms.org/)**: companion site for the textbook by Pevzner and Compeau, with online courses and exercises; exceptionally clear on algorithms.
- **[Modern Statistics for Modern Biology](https://www.huber.embl.de/msmb/)**: by Susan Holmes and Wolfgang Huber, free online; the statistical mindset bioinformatics actually needs.
- **[Bioconductor books](https://bioconductor.org/books/)**: official Bioconductor book library — the authoritative reference for R-based bioinformatics, many titles readable free online.
- **[R for Data Science (2nd ed.)](https://r4ds.hadley.nz/)**: by Hadley Wickham et al., free online; modern R for data work — the best place to build foundations.
- **[Biostar Handbook](https://www.biostarhandbook.com/)**: a systematic, practice-oriented bioinformatics tutorial with many reproducible command-line examples.
- **[ICourse163 (中国大学 MOOC)](https://www.icourse163.org/)**: Chinese university open-course platform; search "生物信息学" for taught-in-Chinese courses you can follow week by week.

To check how much you have actually absorbed, work through **[Rosalind](https://rosalind.info)** — listed above under English resources — by algorithm topic.

## How to use

0. Code convention: command-line / tool steps use **bash** (language-neutral — BLAST, mafft, samtools are shell programs); **data-wrangling, plotting and stats** sections show both **R and Python** — pick either.
1. Build the big picture here first, then pick 1–2 of the projects above to go deep.
2. Stuck on the command line? Check learn-genomics-in-linux and DTC-Bioinformatic-Course first.
3. Want to practice programming? Go to Rosalind; want Chinese videos? The Skills Tree Bilibili channel.
4. Respect each project's open-source license and attribution requirements.
