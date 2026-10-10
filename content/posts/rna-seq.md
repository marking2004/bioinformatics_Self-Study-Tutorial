---
title: "RNA-seq 实战：从原始读数到差异表达基因"
date: "2026-10-05"
weight: 70
category: "组学实战"
meta: "组学 · 约 20 分钟"
draft: "false"
summary: "RNA-seq 用来回答一个问题：'哪些基因在哪种条件下表达得更多 / 更少？'这一课走通一条精简但真实的流程——从原始读数（fastq）一路到差异表达基因，并画出你的第一张火山图。"
---

<p>RNA-seq 用来回答一个问题："哪些基因在哪种条件下表达得更多 / 更少？"这一课走通一条精简但真实的流程——从原始读数（fastq）一路到差异表达基因，并画出你的第一张火山图。</p>
          <h2>1. 流程总览</h2>
          <ul>
            <li>原始读数（fastq）→ <strong>质控</strong>（FastQC）</li>
            <li>→ <strong>比对</strong>到参考基因组（HISAT2）</li>
            <li>→ <strong>定量</strong>（featureCounts）</li>
            <li>→ <strong>差异分析</strong>（DESeq2）→ 可视化</li>
          </ul>
          <h2>2. 质控：先看数据干不干净</h2>
          <pre><code>fastqc sample_R1.fastq.gz sample_R2.fastq.gz
multiqc .     # 把多个样本的报告汇总成一页</code></pre>
          <p>重点看碱基质量是否随读长衰减、是否有接头污染。脏数据不处理，后面全白做。</p>
          <h2>3. 比对与定量</h2>
          <pre><code># 比对到参考基因组，输出排序后的 bam
hisat2 -x genome_index -1 sample_R1.fq -2 sample_R2.fq \
  | samtools sort -o sample.bam

# 按基因（gtf 注释）计数
featureCounts -a genes.gtf -o counts.txt sample.bam</code></pre>
          <h2>4. 差异表达（R + DESeq2）</h2>
          <pre><code>library(DESeq2)
dds <- DESeqDataSetFromMatrix(countData, colData, ~ condition)
dds <- DESeq(dds)
res <- results(dds, alpha = 0.05)
summary(res)        # 看看上调 / 下调了多少个基因</code></pre>
          <p><code>alpha = 0.05</code> 是显著性阈值；DESeq2 会自动做归一化和多重检验校正，不用你手动算。</p>
          <h2>5. 画出第一张火山图</h2>
          <pre><code>library(ggplot2)
res$log10p <- -log10(res$padj)
ggplot(res, aes(log2FoldChange, log10p)) +
  geom_point(alpha = .4) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed")</code></pre>
          <p>横轴是表达变化倍数（log2），纵轴是显著性（−log10 校正 p 值）。右上 / 右下的点，就是值得追的候选基因。</p>
          <h2>小结</h2>
          <p>一条 RNA-seq 流程里藏着太多细节（批次效应、归一化、多重检验），这一课只画骨架。但只要你亲手跑通一次，以后再读论文、听方法，就不再是听黑话了。</p>


## 迷你实战

用 fastqc 看测序质量，再用 salmon 做定量（示例用你自己的双端数据）：

```bash
fastqc reads_1.fastq.gz reads_2.fastq.gz
salmon index -t transcriptome.fa -i index
salmon quant -i index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -o quant
```

观察：`quant/quant.sf` 每行的 `NumReads` / `TPM` 就是该转录本表达量。真实数据去 GEO 下 SRR 编号后走同一流程。
