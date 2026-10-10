---
title: "实验 9：序列拼接与基因预测"
date: "2026-10-10"
weight: 90
category: "基因组学"
meta: "组学 · 约 55 分钟"
module: "genomics"
draft: false
summary: "测序得到的是上千万条短片段，要拼回基因组才知道基因在哪。本实验走完质控—拼接—评估—基因预测—ORF 查找，并说清 N50 该怎么看、预测结果该怎么信。"
---

> 所属模块：[核酸序列分析与基因组学](../posts/genomics.html)

## 一、实验目的

<ul>
  <li>理解从 reads 到 contig / scaffold 的拼接逻辑与它的固有局限；</li>
  <li>会用 QUAST、BUSCO 评估拼接质量，正确理解 N50 的含义；</li>
  <li>区分<strong>从头预测</strong>与<strong>基于证据</strong>两种基因预测路线，并分别实操；</li>
  <li>会用在线与命令行工具查找 ORF 并完成翻译。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>fastp / FastQC</td><td>质控与过滤</td><td><a href="https://github.com/OpenGene/fastp" target="_blank" rel="noopener">fastp</a> · <a href="https://www.bioinformatics.babraham.ac.uk/projects/fastqc/" target="_blank" rel="noopener">FastQC</a></td></tr>
    <tr><td>SPAdes / Flye</td><td>短读长 / 长读长拼接</td><td><a href="https://cab.spbu.ru/software/spades/" target="_blank" rel="noopener">SPAdes</a> · <a href="https://github.com/fenderglass/Flye" target="_blank" rel="noopener">Flye</a></td></tr>
    <tr><td>QUAST / BUSCO</td><td>拼接质量与完整性评估</td><td><a href="https://quast.sourceforge.net/quast" target="_blank" rel="noopener">QUAST</a> · <a href="https://busco.ezlab.org/" target="_blank" rel="noopener">BUSCO</a></td></tr>
    <tr><td>Prodigal / Augustus</td><td>原核 / 真核基因预测</td><td><a href="https://github.com/hyattpd/Prodigal" target="_blank" rel="noopener">Prodigal</a> · <a href="https://bioinf.uni-greifswald.de/augustus/" target="_blank" rel="noopener">Augustus</a></td></tr>
    <tr><td>NCBI ORF Finder</td><td>在线查开放阅读框</td><td><a href="https://www.ncbi.nlm.nih.gov/orffinder/" target="_blank" rel="noopener">ORF Finder</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 质控**

```bash
fastqc -o qc/ reads_R1.fastq.gz reads_R2.fastq.gz     # 看报告
fastp -i reads_R1.fastq.gz -I reads_R2.fastq.gz \
      -o clean_R1.fastq.gz -O clean_R2.fastq.gz \
      --detect_adapter_for_pe --cut_tail --cut_mean_quality 20
```

这一步决定后续一切的质量。接头没去干净、低质量尾没剪，会直接拉低拼接连续性。

**2. 拼接**

```bash
# 细菌等小基因组（Illumina 双端）
spades.py -1 clean_R1.fastq.gz -2 clean_R2.fastq.gz -o spades_out -t 8

# 长读长（Nanopore / PacBio）
flye --nano-raw reads.fastq.gz --out-dir flye_out --genome-size 5m -t 8
```

> 拼接器按数据类型分工：<strong>短读长用 SPAdes，长读长用 Flye / Canu</strong>。混用会因错误率模型不匹配而结果很差。

**3. 评估拼接质量**

```bash
quast.py -o quast_out -R ref.fasta spades_out/scaffolds.fasta
busco -i spades_out/scaffolds.fasta -l bacteria_odb10 -m genome -o busco_out
```

**4. 基因预测**

```bash
# 原核：Prodigal，简单且准
prodigal -i scaffolds.fasta -a proteins.faa -d genes.fna -o genes.gff -f gff

# 真核：Augustus，需要选近缘物种的模型
augustus --species=arabidopsis scaffolds.fasta > augustus.gff
```

<p>真核基因有内含子，必须依赖物种特异的预训练模型；模型选错会漏掉大量外显子。</p>

**5. 查找 ORF 并翻译（小规模最直观）**

打开 <a href="https://www.ncbi.nlm.nih.gov/orffinder/" target="_blank" rel="noopener">NCBI ORF Finder</a>，粘贴序列，设定最小 ORF 长度与遗传密码表，即可看到所有候选阅读框与翻译结果。命令行等价做法：

```bash
getorf -sequence input.fasta -outseq orfs.fasta -minsize 300 -find 3
transeq -sequence genes.fna -outseq proteins.fasta -frame 1
```

**6. 功能注释**

```bash
blastp -query proteins.faa -db uniprot -evalue 1e-5 -outfmt 6 > ann.tsv
interproscan.sh -i proteins.faa -f tsv -o ipr.tsv
```

## 四、结果判读

<ul>
  <li><strong>N50 是什么</strong>：把所有 contig 按长度从大到小累加，累计达到总长 50% 时那条 contig 的长度。它反映<strong>连续性</strong>，越大越好——但只看 N50 会被"少数长 contig + 大量碎片"骗到，必须同时看 contig 总数与总长。</li>
  <li><strong>BUSCO 完整性</strong>：报告 Complete / Single / Duplicated / Fragmented / Missing 五类。Complete 比例越高说明核心基因越齐全；<strong>Duplicated 偏高</strong>常提示拼接产生了冗余（如杂合区域被拆成两条）。</li>
  <li><strong>与预期基因组大小比较</strong>：总长远大于预期通常是污染或冗余；远小于预期说明覆盖不足或高重复区丢失。</li>
  <li><strong>预测基因数合理性</strong>：与近缘物种比较，数量差一倍以上就要检查模型与输入。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>拼完不评估直接用</strong>：N50 高不代表没有错拼（misassembly），BUSCO 与 QUAST 一起看才稳。</li>
  <li><strong>基因预测用错模型</strong>：真核用原核参数（或反之）会得到大量假基因。</li>
  <li><strong>把预测结果当实验事实</strong>：ab initio 预测是<strong>假设</strong>，需要转录组或同源蛋白证据支持才算可靠。</li>
  <li><strong>忽略重复区域</strong>：短读长在重复区必然断裂，contig 边界常落在重复序列处。</li>
  <li><strong>磁盘与内存</strong>：拼接是全流程最吃资源的一步，细菌基因组尚可在笔记本跑，真核基因组需要服务器。</li>
</ul>

## 六、练习

<ol>
  <li>对一对双端数据跑 fastp，比较过滤前后的 reads 数与平均质量。</li>
  <li>用 SPAdes 拼接（可用公开的小基因组数据集），记录 contig 数与 N50。</li>
  <li>跑 QUAST 与 BUSCO，写出完整度百分比与碎片化比例。</li>
  <li>用 Prodigal 预测基因，报告基因数量与平均长度。</li>
  <li>（选做）用 NCBI ORF Finder 验证其中一条预测基因，比较两者起点是否一致。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://cab.spbu.ru/software/spades/" target="_blank" rel="noopener">SPAdes 手册</a></li>
  <li><a href="https://busco.ezlab.org/busco_userguide.html" target="_blank" rel="noopener">BUSCO 用户指南</a></li>
  <li><a href="https://www.ncbi.nlm.nih.gov/orffinder/" target="_blank" rel="noopener">NCBI ORF Finder</a></li>
  <li><a href="https://bioinf.uni-greifswald.de/augustus/" target="_blank" rel="noopener">Augustus 文档</a></li>
</ul>
