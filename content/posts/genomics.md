---
title: "核酸序列分析与基因组学"
date: "2026-10-05"
weight: 60
category: "基因组学"
meta: "组学 · 约 25 分钟"
draft: "false"
summary: "基因组学关心'整条 DNA / 整套序列'能告诉我们什么。本模块把常见的子方向串起来，方便你按需要取用。"
---

<p>基因组学关心"整条 DNA / 整套序列"能告诉我们什么。本模块把常见的子方向串起来，方便你按需要取用。</p>
          <h2>1. 测序数据处理</h2>
          <ul>
            <li><strong>质控与过滤</strong>：fastp（一步完成去接头、质控、剪切）；</li>
            <li><strong>组装</strong>：二代用 SPAdes / SOAPdenovo，三代用 Canu / Flye；</li>
            <li><strong>比对到参考</strong>：BWA（短读）、minimap2（长读 / 跨物种）。</li>
          </ul>
          <pre><code>fastp -i r1.fq -o c1.fq -I r2.fq -O c2.fq
bwa mem ref.fa c1.fq c2.fq | samtools sort &gt; sample.bam</code></pre>
          <h2>2. 共线性分析</h2>
          <p>比较两个基因组"哪些区块对应、是否有重排"。工具：MCscan（Python）、JDart、SynVisio（可视化）。常用于看物种形成后的染色体重排。</p>
          <h2>3. 基因 / 蛋白家族分析</h2>
          <ul>
            <li><strong>OrthoFinder</strong>：推断直系同源 / 旁系同源组，输出基因家族与系统发育；</li>
            <li><strong>Pfam / InterPro</strong>：家族与结构域注释；</li>
            <li><strong>CAFE</strong>：检验家族扩张 / 收缩（结合物种树）。</li>
          </ul>
          <h2>4. SNP 与分子标记、遗传多样性</h2>
          <ul>
            <li><strong>Calling</strong>：GATK（标准流程）、freebayes；</li>
            <li><strong>群体统计</strong>：vcftools / PLINK 算 π、Fst、Tajima's D，看选择信号与多样性；</li>
            <li><strong>分子标记</strong>：SSR、SNP 芯片用于育种与指纹。</li>
          </ul>
          <pre><code>vcftools --vcf snps.vcf --weir-fst-pop popA.txt \
  --weir-fst-pop popB.txt --out fst</code></pre>
          <h2>5. 各类小 RNA 分析</h2>
          <ul>
            <li><strong>miRNA</strong>：miRBase 注释、sRNAbench / miRDeep2 预测新 miRNA；</li>
            <li><strong>siRNA / piRNA</strong>：看长度分布与来源（转座子 / 异染色质）；</li>
            <li><strong>lncRNA</strong>：按长度、外显子结构、编码潜力（CPC2 / CNCI）筛选。</li>
          </ul>
          <blockquote>基因组分析的坑多在"数据不对"：污染、杂合、批次、样品混淆。任何结论前，先做基础 QC 与样本相关性（PCA）检查。</blockquote>


## 迷你实战

用 samtools 看一个 BAM 的基本统计（先要有比对结果）：

```bash
samtools flagstat aln.bam
samtools idxstats aln.bam
```

观察：`flagstat` 里 mapped % 表示比对率；`idxstats` 给出每条参考序列的覆盖深度。处理 FASTA/A 用 `seqkit` 同理。
