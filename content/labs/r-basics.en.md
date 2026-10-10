---
title: "Lab 2: R Basics and Data Visualisation"
date: "2026-10-10"
weight: 20
category: "Programming"
meta: "Basics · ~45 min"
module: "programming"
draft: false
summary: "R is the workhorse of downstream omics analysis. This lab covers data structures, file I/O, installing from CRAN and Bioconductor, and drawing your first presentable figure with ggplot2."
---

> Module: [Programming Basics: R and Python](../posts/programming.html)

## 1. Goals

<ul>
  <li>Get comfortable with vectors, data frames and factors;</li>
  <li>Read and write CSV/TSV, filter, summarise and run a simple statistical test;</li>
  <li>Understand the two package channels, <strong>CRAN and Bioconductor</strong>;</li>
  <li>Produce scatter, bar and box plots with ggplot2.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>R</td><td>the language</td><td><a href="https://www.r-project.org/" target="_blank" rel="noopener">r-project.org</a></td></tr>
    <tr><td>RStudio / Posit</td><td>IDE</td><td><a href="https://posit.co/download/rstudio-desktop/" target="_blank" rel="noopener">download</a></td></tr>
    <tr><td>CRAN</td><td>general package repository</td><td><a href="https://cran.r-project.org/" target="_blank" rel="noopener">cran.r-project.org</a></td></tr>
    <tr><td>Bioconductor</td><td>omics package repository</td><td><a href="https://www.bioconductor.org/" target="_blank" rel="noopener">bioconductor.org</a></td></tr>
    <tr><td>ggplot2</td><td>plotting</td><td><a href="https://ggplot2.tidyverse.org/" target="_blank" rel="noopener">ggplot2.tidyverse.org</a></td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Install and start**

```r
R.version.string        # version
getwd()                 # working directory
setwd("~/lab02")        # set it
```

**2. Data structures**

```r
x <- c(1, 3, 5, 7, 9)          # vector
x * 2                          # vectorised, no loop needed
df <- data.frame(
  gene = c("AtNHX1", "AtSOS1", "AtHKT1"),
  tpm  = c(45.2, 12.8, 88.6),
  tissue = c("root", "leaf", "root")
)
df$gene                        # a column
df[df$tpm > 20, ]              # filter rows
str(df)                        # structure
summary(df$tpm)                # summary statistics
```

> `tissue` becomes a factor automatically. That is what you want for grouping, but convert with `as.character()` before string operations.

**3. File I/O**

```r
dat <- read.csv("counts.csv", row.names = 1)         # comma separated
dat <- read.delim("counts.tsv", row.names = 1)       # tab separated
write.csv(df, "result.csv", row.names = FALSE)
```

**4. Installing packages: two channels, do not mix**

```r
install.packages("ggplot2")                          # CRAN
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("DESeq2")                       # Bioconductor
library(ggplot2)
```

> Bioconductor releases are tied to R versions. Check its <a href="https://www.bioconductor.org/about/release-announcements/" target="_blank" rel="noopener">release announcements</a> before upgrading R, or old packages will not install.

**5. Plotting**

```r
p <- ggplot(df, aes(x = tissue, y = tpm, fill = tissue)) +
  geom_boxplot() +
  geom_point(position = position_jitter(width = .15), size = 2) +
  labs(title = "Gene expression by tissue", x = "Tissue", y = "TPM") +
  theme_bw()
ggsave("boxplot.png", p, width = 5, height = 4, dpi = 300)
```

**6. A statistical test**

```r
t.test(tpm ~ tissue, data = df)
```

## 4. Reading the results

<ul>
  <li>In <code>str()</code> output, <code>num</code> is numeric, <code>chr</code> character, <code>Factor w/ 2 levels</code> a factor. Wrong types cause most beginner errors.</li>
  <li><code>summary()</code> gives min, quartiles, median, mean and max — read it first to spot outliers or all-zero columns.</li>
  <li>A <code>p-value</code> below 0.05 only says the difference is unlikely to be random noise; it is <strong>not</strong> the same as biological importance. Always check the fold change too.</li>
  <li>Before <code>ggsave</code>, look at the plot. A blank canvas usually means empty data or a mistake in the <code>aes</code> mapping.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Install fails halfway</strong>: usually missing system libraries for compilation. On Linux install dev packages first; the easiest route is conda's R with common packages.</li>
  <li><strong>Mojibake</strong>: UTF-8 files can garble on Windows. Pass <code>fileEncoding = "UTF-8"</code>, or standardise the locale.</li>
  <li><strong>Path separators</strong>: Windows <code>\</code> is an escape character in R strings. Use <code>/</code> or <code>\\</code>.</li>
  <li><strong>Overwriting raw data</strong>: assigning a filtered result back to the same name loses the original. Keep a <code>raw</code> copy.</li>
</ul>

## 6. Exercises

<ol>
  <li>Build a data frame of 6 genes x 3 samples and compute each gene's mean.</li>
  <li>Write it to TSV, read it back, and confirm row names did not shift.</li>
  <li>Install <code>clusterProfiler</code> with <code>BiocManager::install()</code>; note how long it took and any errors.</li>
  <li>Draw a scatter plot of sample A against sample B and add a <code>y = x</code> reference line.</li>
  <li>(Optional) Run a t-test between two groups and state the null hypothesis, p-value and conclusion in one sentence each.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://r4ds.hadley.nz/" target="_blank" rel="noopener">R for Data Science (online)</a></li>
  <li><a href="https://posit.co/resources/cheatsheets/" target="_blank" rel="noopener">Official RStudio cheatsheets</a></li>
  <li><a href="https://www.bioconductor.org/packages/release/BiocViews.html" target="_blank" rel="noopener">Bioconductor package index</a></li>
</ul>
