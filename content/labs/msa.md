---
title: "实验 7：多序列联配与结果可视化"
date: "2026-10-10"
weight: 70
category: "序列分析"
meta: "序列 · 约 50 分钟"
module: "msa"
draft: false
summary: "把同源序列上下对齐，才能看出哪些位置在进化中被保留下来。本实验用 MAFFT 做联配，学会去冗余、修剪与可视化，并判断一份联配结果是否可信。"
---

> 所属模块：[多序列比对与结果可视化](../posts/msa.html)

## 一、实验目的

<ul>
  <li>理解多序列比对（MSA）的目的：找出跨物种或跨家族<strong>保守的列</strong>；</li>
  <li>会用在线与命令行两种方式做联配，知道 MAFFT / MUSCLE / Clustal Omega 各自的定位；</li>
  <li>掌握结果<strong>去冗余、修剪与可视化</strong>的完整流程；</li>
  <li>能判断一份联配结果是否可用于后续建树或功能位点分析。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>MAFFT</td><td>主流联配程序，快速且准确</td><td><a href="https://mafft.cbrc.jp/alignment/software/" target="_blank" rel="noopener">软件页</a> · <a href="https://mafft.cbrc.jp/alignment/server/" target="_blank" rel="noopener">在线服务</a></td></tr>
    <tr><td>MUSCLE / Clustal Omega</td><td>备选联配程序</td><td><a href="https://www.ebi.ac.uk/Tools/msa/" target="_blank" rel="noopener">EBI 在线</a></td></tr>
    <tr><td>trimAl</td><td>修剪不可靠区段</td><td><a href="http://trimal.cgenomics.org/" target="_blank" rel="noopener">trimal</a></td></tr>
    <tr><td>Jalview</td><td>本地查看与编辑联配</td><td><a href="https://www.jalview.org/" target="_blank" rel="noopener">jalview.org</a></td></tr>
    <tr><td>WebLogo / ESPript</td><td>保守性图形化</td><td><a href="https://weblogo.berkeley.edu/" target="_blank" rel="noopener">WebLogo</a> · <a href="https://espript.ibcp.fr/" target="_blank" rel="noopener">ESPript</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 准备输入：同源且不过度冗余**

<p>联配的前提是<strong>同源</strong>。输入序列通常来自 BLAST 的 top hits，但要注意：</p>

<ul>
  <li>去掉几乎完全相同的重复序列（冗余会让联配偏向大家族）；</li>
  <li>确认序列方向一致，反向的要先反向互补；</li>
  <li>序列数量以 10–50 条为宜：太少保守性不可靠，太多联配质量下降。</li>
</ul>

```bash
seqkit seq -r -p seqs.fasta > rc.fasta          # 反向互补（如需）
seqkit rmdup -s seqs.fasta > dedup.fasta        # 按序列去冗余
seqkit stats dedup.fasta
```

**2. 在线联配（少量序列最快）**

打开 <a href="https://mafft.cbrc.jp/alignment/server/" target="_blank" rel="noopener">MAFFT 在线服务</a>，粘贴 FASTA，策略保持默认（<code>--auto</code>），提交后用 Jalview 打开结果查看。

**3. 命令行联配**

```bash
mafft --auto --thread 4 input.fasta > aligned.fasta
muscle -align input.fasta -output aligned.fasta          # 备选
```

常用参数：<code>--maxiterate 1000 --localpair</code>（精度优先，适合少量序列）、<code>--auto</code>（自动权衡）、<code>--thread</code>（并行）。

**4. 修剪不可靠区段**

```bash
trimal -in aligned.fasta -out trimmed.fasta -automated1
```

gap 多、局部混乱的区段会干扰建树，一般建议修剪；做功能位点展示时可保留全长以便对照。

**5. 可视化与保守性分析**

<ul>
  <li><strong>Jalview</strong>：本地查看，可按列着色（如按疏水性、按保守度），直接看出哪些列完全一致；</li>
  <li><strong>WebLogo</strong>：把每个位置的信息量画成字母高度，越高的位置越保守；</li>
  <li><strong>ESPript</strong>：出版级图形，可叠加二级结构信息。</li>
</ul>

**6. 转成其他格式**

```bash
seqkit convert --to phylip aligned.fasta > aligned.phy   # 供建树程序读取
```

## 四、结果判读

<ul>
  <li><strong>看列的一致性</strong>：整列完全相同的残基，往往对应功能位点或结构核心；这些列是后续突变实验的首选靶点。</li>
  <li><strong>看 gap 的分布</strong>：如果 gap 集中在少数几条序列的同一段，说明它们可能多了一段插入序列，或这一段本身非同源。</li>
  <li><strong>看两端</strong>：联配两端常常参差不齐（因为序列长度不一），这是正常的；若中段也大面积错开，多半是输入序列不同源。</li>
  <li><strong>可信度自检</strong>：把联配结果用不同程序（MAFFT 与 MUSCLE）各跑一次，若一致的列基本重合，结果较可靠。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>把非同源序列塞进去</strong>：MSA 只会机械地对齐，不会判断同源性。结果看起来有模有样，结论却全错。</li>
  <li><strong>序列方向不一致</strong>：一条反向的序列会彻底打乱联配。跑之前用联配工具检查，或用 <code>seqkit</code> 统一方向。</li>
  <li><strong>过度依赖默认参数</strong>：远缘序列用默认参数常常对不齐，需换 <code>--localpair --maxiterate</code> 等高精度策略。</li>
  <li><strong>拿带 gap 的原长序列直接建树</strong>：不同程序对 gap 的处理不同，通常修剪后再建树更稳妥。</li>
</ul>

## 六、练习

<ol>
  <li>用 BLAST 找一个基因家族，收集 10–20 条同源蛋白序列，记录筛选标准。</li>
  <li>用 MAFFT 联配，报告联配后的列数与完全保守的列数。</li>
  <li>用 trimAl 修剪，比较修剪前后的长度差异。</li>
  <li>用 Jalview 打开，标注出你认为最可能的功能保守位点，说明理由。</li>
  <li>（选做）把结果提交 WebLogo，截一张保守性图，说明哪个位置信息量最高。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://mafft.cbrc.jp/alignment/software/" target="_blank" rel="noopener">MAFFT 官方文档</a></li>
  <li><a href="https://www.jalview.org/help/html/features.html" target="_blank" rel="noopener">Jalview 功能说明</a></li>
  <li><a href="http://trimal.cgenomics.org/" target="_blank" rel="noopener">trimAl 使用说明</a></li>
</ul>
