---
title: "实验 10：基因组可视化与浏览器操作"
date: "2026-10-10"
weight: 100
category: "基因组学"
meta: "组学 · 约 45 分钟"
module: "genomics"
draft: false
summary: "基因组数据只有落到坐标上才看得懂。本实验带你用 Ensembl、UCSC 与本地 IGV 浏览基因结构、比对覆盖度与变异，并讲清坐标与版本这两个最容易出错的地方。"
---

> 所属模块：[核酸序列分析与基因组学](../posts/genomics.html)

## 一、实验目的

<ul>
  <li>理解基因组浏览器"以坐标为主轴、以 track 为图层"的设计；</li>
  <li>能在 Ensembl / UCSC / NCBI 上找到基因的转录本、外显子与同源信息；</li>
  <li>会用 <strong>IGV</strong> 在本地查看比对结果与覆盖度峰；</li>
  <li>掌握自定义 track（BED / GFF）的坐标规则，避免差一位的经典错误。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>Ensembl</td><td>基因结构与注释浏览</td><td><a href="https://www.ensembl.org/" target="_blank" rel="noopener">ensembl.org</a></td></tr>
    <tr><td>UCSC Genome Browser</td><td>多 track 叠加、BLAT</td><td><a href="https://genome.ucsc.edu/" target="_blank" rel="noopener">genome.ucsc.edu</a></td></tr>
    <tr><td>NCBI Genome Data Viewer</td><td>NCBI 视角的基因组浏览</td><td><a href="https://www.ncbi.nlm.nih.gov/gdv/" target="_blank" rel="noopener">GDV</a></td></tr>
    <tr><td>IGV</td><td>本地查看比对与变异</td><td><a href="https://igv.org/" target="_blank" rel="noopener">igv.org</a></td></tr>
    <tr><td>JBrowse 2</td><td>可自建的网页浏览器</td><td><a href="https://jbrowse2.jbrowse.org/" target="_blank" rel="noopener">JBrowse 2</a></td></tr>
    <tr><td>samtools</td><td>比对文件排序与索引</td><td><a href="https://www.htslib.org/" target="_blank" rel="noopener">htslib</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 先固定基因组版本**

<p>开始之前务必确认用的是哪一版基因组（如人类 <code>GRCh38/hg38</code> 与 <code>GRCh37/hg19</code>）。<strong>不同版本的坐标不能互用</strong>，这是最常见的返工原因。</p>

**2. 在 Ensembl 上读一个基因**

搜索基因名 → 进入 Gene 页，重点看：
<ul>
  <li><em>Transcripts</em>：一个基因常有多个转录本（ isoform ），只有标注 <em>canonical</em> 的是默认代表；</li>
  <li>转录本图：实心块是外显子（CDS 更粗、UTR 更细），细线是内含子；</li>
  <li>方向：箭头向左表示基因在负链，序列需反向互补读取。</li>
</ul>

**3. 在 UCSC 上叠加 track**

定位到区域后，在下方 track 区勾选需要的图层（如 <em>Refseq Genes</em>、<em>dbSNP</em>、<em>Conservation</em>）。用 <em>BLAT</em> 可以把一段序列快速定位回基因组。

**4. 用 IGV 看本地数据**

```bash
samtools faidx ref.fasta                    # 为参考序列建索引
samtools sort -@ 4 -o sorted.bam aln.sam    # SAM 转 BAM 并排序
samtools index sorted.bam                   # 建 .bai 索引（载入 IGV 必需）
```

IGV 操作：<em>Genomes → Load Genome from File</em> 载入 <code>ref.fasta</code>，再 <em>File → Load from File</em> 载入 <code>sorted.bam</code> 与注释 <code>genes.gff</code>。

**5. 上传自定义 track**

<ul>
  <li><strong>BED</strong>：0-based、半开区间，三列必填（chrom, start, end）；</li>
  <li><strong>GFF / GTF</strong>：1-based、闭区间，第 9 列是属性串。</li>
</ul>

```bash
# 从 BAM 直接看某个区间的比对情况
samtools view -h sorted.bam chr1:1000000-1001000 | head
```

## 四、结果判读

<ul>
  <li><strong>覆盖度峰</strong>：IGV 顶部灰色柱状图是覆盖深度。某个外显子上有连续高覆盖，说明该区域表达量高；若峰只出现在部分外显子，可能是 isoform 差异或降解。</li>
  <li><strong>跨内含子的 reads</strong>：reads 中间出现"缺口"（N 或细线跨过），表示跨越了剪接位点，是转录本存在的直接证据。</li>
  <li><strong>变异位点</strong>：IGV 里彩色竖条表示与参考不同的碱基。颜色比例接近 50/50 多为杂合，接近 100% 多为纯合；低于 20% 要警惕测序错误。</li>
  <li><strong>链的判断</strong>：基因图上的箭头方向决定是否需反向互补，做引物或取序列时必须对齐。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>坐标差一位</strong>：BED 是 0-based 半开、GFF 是 1-based 闭区间。两者互转忘记加/减 1，会导致区段偏移一个碱基，做克隆时可能是致命的。</li>
  <li><strong>基因组版本混用</strong>：从论文拿到 hg19 坐标却在 hg38 上看，位置完全不同。交叉验证时用 <em>LiftOver</em> 转换。</li>
  <li><strong>BAM 没索引</strong>：IGV 无法随机访问，载入失败或极慢。必须 <code>samtools index</code>。</li>
  <li><strong>文件太大</strong>：全基因组覆盖度文件建议转 BigWig 后再载入，直接拖 BAM 在大基因组上会卡死。</li>
  <li><strong>只看默认转录本</strong>：一个基因可能有十几个转录本，结论依赖哪一个要写清楚。</li>
</ul>

## 六、练习

<ol>
  <li>在 Ensembl 找一个你熟悉的基因，记录其 ID、位置、链方向与转录本数量。</li>
  <li>截取该基因一个外显子的序列，用 UCSC BLAT 定位，验证坐标一致。</li>
  <li>用 samtools 为一份比对文件建立索引，载入 IGV 截图，标出一个覆盖度峰。</li>
  <li>手工写一个 3 行的 BED 文件并载入，确认显示位置与你预期的坐标一致。</li>
  <li>（选做）比较同一基因在 Ensembl 与 NCBI GDV 上的转录本数量是否一致，并解释差异。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://igv.org/doc/desktop/" target="_blank" rel="noopener">IGV 桌面版文档</a></li>
  <li><a href="https://genome.ucsc.edu/goldenPath/help/hgTracksHelp.html" target="_blank" rel="noopener">UCSC 浏览器使用帮助</a></li>
  <li><a href="https://www.ensembl.org/info/website/tutorials/index.html" target="_blank" rel="noopener">Ensembl 教程</a></li>
  <li><a href="https://www.htslib.org/doc/samtools.html" target="_blank" rel="noopener">samtools 文档</a></li>
</ul>
