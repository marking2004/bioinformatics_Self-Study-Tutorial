---
title: "实验 11：转录组分析（质控到富集）"
date: "2026-10-10"
weight: 110
category: "转录组"
meta: "组学 · 约 70 分钟"
module: "rna-seq"
draft: false
summary: "转录组是本科阶段最常做的组学分析。本实验走完整条链路：质控 → 比对/免比对定量 → 计数 → 差异表达 → 富集，并指出 FPKM、重复数与批次效应这几个高频失分点。"
---

> 所属模块：[RNA-seq 分析](../posts/rna-seq.html)

## 一、实验目的

<ul>
  <li>掌握 RNA-seq 的标准链路与每一步的输入输出；</li>
  <li>能独立完成质控、比对（或免比对定量）与基因水平计数；</li>
  <li>用 <strong>DESeq2</strong> 做差异表达，并正确解释 padj 与 log2FC；</li>
  <li>用 <strong>clusterProfiler</strong> 做 GO / KEGG 富集，理解背景基因集的意义。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>fastp / FastQC / MultiQC</td><td>质控与汇总报告</td><td><a href="https://github.com/OpenGene/fastp" target="_blank" rel="noopener">fastp</a> · <a href="https://multiqc.info/" target="_blank" rel="noopener">MultiQC</a></td></tr>
    <tr><td>HISAT2 / STAR</td><td>基因组比对</td><td><a href="https://daehwankimlab.github.io/hisat2/" target="_blank" rel="noopener">HISAT2</a> · <a href="https://github.com/alexdobin/STAR" target="_blank" rel="noopener">STAR</a></td></tr>
    <tr><td>Salmon / kallisto</td><td>免比对转录本定量</td><td><a href="https://salmon.readthedocs.io/" target="_blank" rel="noopener">Salmon</a> · <a href="https://pachterlab.github.io/kallisto/" target="_blank" rel="noopener">kallisto</a></td></tr>
    <tr><td>featureCounts</td><td>基因水平计数</td><td><a href="https://subread.sourceforge.net/" target="_blank" rel="noopener">Subread</a></td></tr>
    <tr><td>DESeq2 / edgeR</td><td>差异表达</td><td><a href="https://bioconductor.org/packages/DESeq2/" target="_blank" rel="noopener">DESeq2</a></td></tr>
    <tr><td>clusterProfiler</td><td>GO / KEGG 富集</td><td><a href="https://bioconductor.org/packages/clusterProfiler/" target="_blank" rel="noopener">clusterProfiler</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 质控**

```bash
fastp -i R1.fq.gz -I R2.fq.gz -o clean_R1.fq.gz -O clean_R2.fq.gz \
      --detect_adapter_for_pe --cut_tail --cut_mean_quality 20 \
      --html qc/sample.html
multiqc qc/ -o qc/multiqc_report.html      # 多样本汇总，先看它
```

**2. 路线 A：比对到基因组**

```bash
hisat2-build genome.fa genome_idx                      # 建索引（只需一次）
hisat2 -x genome_idx -1 clean_R1.fq.gz -2 clean_R2.fq.gz -S aln.sam -p 8
samtools sort -@ 4 -o sorted.bam aln.sam && samtools index sorted.bam
featureCounts -T 8 -p -a annotation.gtf -o counts.txt sorted.bam
```

**3. 路线 B：免比对定量（更快）**

```bash
salmon index -t transcripts.fa -i tx_idx
salmon quant -i tx_idx -l A -1 clean_R1.fq.gz -2 clean_R2.fq.gz -o quant/sample
```

<p>有高质量参考转录组时，Salmon 速度快得多；需要看剪接、新转录本或可变剪切时，走比对路线。</p>

**4. 差异表达（DESeq2）**

```r
library(DESeq2)
cts <- read.delim("counts.txt", row.names = 1, check.names = FALSE)
cts <- cts[, 6:ncol(cts)]                       # 去掉 featureCounts 的前几列注释
coldata <- data.frame(condition = factor(c("ctrl","ctrl","treat","treat")))
rownames(coldata) <- colnames(cts)

dds <- DESeqDataSetFromMatrix(cts, coldata, ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast = c("condition", "treat", "ctrl"))
res <- res[order(res$padj), ]
write.csv(as.data.frame(res), "DEG.csv")

# 常用图
plotPCA(vst(dds), intgroup = "condition")
```

**5. 富集分析**

```r
library(clusterProfiler)
library(org.At.tair.db)                        # 拟南芥；人类用 org.Hs.eg.db
deg <- rownames(res[res$padj < 0.05 & abs(res$log2FoldChange) > 1, ])

ego <- enrichGO(gene = deg, OrgDb = org.At.tair.db, keyType = "TAIR",
                ont = "BP", pAdjustMethod = "BH", qvalueCutoff = 0.05)
dotplot(ego, showCategory = 20)

kegg <- enrichKEGG(gene = deg, organism = "ath", pAdjustMethod = "BH", qvalueCutoff = 0.05)
```

## 四、结果判读

<ul>
  <li><strong>比对率</strong>：总比对率一般应在 70–90% 以上。过低提示污染、参考基因组选错或接头未去；<strong>多重比对率过高</strong>说明重复序列或基因家族干扰。</li>
  <li><strong>用原始计数做差异表达</strong>：DESeq2 / edgeR 内部自带标准化，输入必须是 raw counts。<strong>不能拿 FPKM/TPM 当输入</strong>。</li>
  <li><strong>看 padj 而不是 pvalue</strong>：几万个基因同时检验，必须做多重校正。常用阈值 <code>padj &lt; 0.05 且 |log2FC| &gt; 1</code>。</li>
  <li><strong>PCA 先于结论</strong>：样本若未按分组聚拢，而是按送样批次聚拢，说明存在<strong>批次效应</strong>，应在设计公式里加入批次项，否则差异基因里混的是批次差异。</li>
  <li><strong>富集看三件事</strong>：校正后的 qvalue、该通路命中的基因数（Count）、以及<strong>背景基因集是否正确</strong>（背景应是所有检测到的基因，不是全基因组）。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>生物学重复不足</strong>：每组至少 3 个重复。n=1 无法估计离散度，DESeq2 结果不可信；n=2 结果极不稳定。</li>
  <li><strong>用 FPKM/TPM 跑差异表达</strong>：这是最常见的错误。这两个指标适合展示表达量，不适合做统计检验。</li>
  <li><strong>注释版本与基因组不匹配</strong>：GTF 与 FASTA 来自不同版本，会导致大量 reads 落在"无基因"区域。</li>
  <li><strong>富集背景集用错</strong>：只用差异基因去富集而不设背景，会夸大某些通路。</li>
  <li><strong>把富集结果当结论</strong>：富集给的是<strong>假设</strong>。真正的功能验证需要实验。</li>
</ul>

## 六、练习

<ol>
  <li>对一份双端数据跑 fastp 与 MultiQC，写出过滤前后 reads 数、Q20/Q30 比例。</li>
  <li>用 HISAT2 比对并统计比对率与多重比对率，判断是否需要换参考。</li>
  <li>用 featureCounts 得到计数矩阵，检查样本间总计数是否量级一致。</li>
  <li>用 DESeq2 做两组比较，报告上调与下调基因数（padj &lt; 0.05）。</li>
  <li>（选做）对差异基因做 GO 富集，挑一条通路说明其生物学含义，并指出本分析的局限。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://bioconductor.org/packages/DESeq2/vignettes/DESeq2.html" target="_blank" rel="noopener">DESeq2 官方 vignette</a></li>
  <li><a href="https://yulab-smu.top/biomedical-knowledge-mining-book/" target="_blank" rel="noopener">clusterProfiler 官方手册</a></li>
  <li><a href="https://salmon.readthedocs.io/en/latest/" target="_blank" rel="noopener">Salmon 文档</a></li>
  <li><a href="https://multiqc.info/" target="_blank" rel="noopener">MultiQC</a></li>
</ul>
