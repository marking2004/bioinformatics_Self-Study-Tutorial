---
title: "实验 13：非编码 RNA——miRNA 鉴定、靶标预测与 ceRNA 网络"
date: "2026-10-10"
weight: 130
category: "转录组"
meta: "组学 · 约 60 分钟"
module: "rna-seq"
draft: false
summary: "miRNA 靠'序列 + 结构'两条证据来判定，靶标预测则注定有假阳性。本实验走完鉴定—预测—验证库比对—ceRNA 建网，并说明哪些结论站得住、哪些只是候选。"
---

> 所属模块：[RNA-seq 分析](../posts/rna-seq.html)

## 一、实验目的

<ul>
  <li>掌握 miRNA 鉴定的两条判据：<strong>序列同源</strong>与<strong>发夹二级结构</strong>；</li>
  <li>会用主流在线工具做靶基因预测，并理解预测结果的局限；</li>
  <li>会用<strong>已验证数据库</strong>给预测结果加权；</li>
  <li>理解 ceRNA 网络的构建逻辑与它需要满足的条件。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>数据库 / 工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>miRBase</td><td>已知 miRNA 序列与命名</td><td><a href="https://www.mirbase.org/" target="_blank" rel="noopener">mirbase.org</a></td></tr>
    <tr><td>RNAfold（ViennaRNA）</td><td>二级结构与最小自由能</td><td><a href="https://www.tbi.univie.ac.at/RNA/" target="_blank" rel="noopener">ViennaRNA</a></td></tr>
    <tr><td>psRNATarget</td><td>植物 miRNA 靶标预测</td><td><a href="https://www.zhaolab.org/psRNATarget/" target="_blank" rel="noopener">psRNATarget</a></td></tr>
    <tr><td>TargetScan / miRanda</td><td>动物靶标预测</td><td><a href="https://www.targetscan.org/" target="_blank" rel="noopener">TargetScan</a></td></tr>
    <tr><td>miRTarBase / starBase</td><td>已实验验证的靶向关系</td><td><a href="https://mirtarbase.cuhk.edu.cn/" target="_blank" rel="noopener">miRTarBase</a> · <a href="https://starbase.sysu.edu.cn/" target="_blank" rel="noopener">starBase</a></td></tr>
    <tr><td>Cytoscape</td><td>网络可视化</td><td><a href="https://cytoscape.org/" target="_blank" rel="noopener">cytoscape.org</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 已知 miRNA 鉴定：先比同源**

```bash
# 用小 RNA 测序 reads 或候选序列，比对到 miRBase 成熟序列库
blastn -query candidates.fasta -db miRBase_mature -evalue 0.01 -outfmt 6
```

<p>与已知 miRNA 完全一致或仅 1–2 个错配的，可直接归入对应家族。注意 miRNA 命名规则：<code>osa-miR156a</code> 中的 <code>osa</code> 是物种、<code>156</code> 是家族号、末尾字母区分拷贝。</p>

**2. 新 miRNA 预测：看能不能形成发夹**

```bash
RNAfold --noPS < precursor.fasta        # 输出二级结构与最小自由能 MFE
```

<p>判定一个新候选是否为 miRNA，通常要求：</p>

<ul>
  <li>前体（约 60–300 nt）能折叠成典型的<strong>发夹结构</strong>；</li>
  <li>成熟序列位于发夹的一条臂上，且两端位置一致（避免大量拖尾）；</li>
  <li>最小自由能足够低（常用指标 MFEI，即 MFE 除以 GC 含量，越高越可信）；</li>
  <li>发夹内部没有大的内环或多分支结构。</li>
</ul>

<p>RNAfold 输出的括号式结构 <code>((((...))))</code> 中，配对的部分越集中说明发夹越规整。</p>

**3. 靶基因预测**

<ul>
  <li><strong>植物</strong>：psRNATarget 提交 miRNA 与候选转录本，看 <em>Expectation</em>（期望值，越小越好）与抑制类型（ cleavage / translation inhibition ）；</li>
  <li><strong>动物</strong>：TargetScan 看种子区匹配与保守性，miRanda 看结合自由能。</li>
</ul>

**4. 用已验证数据库过滤**

把预测结果拿到 <a href="https://mirtarbase.cuhk.edu.cn/" target="_blank" rel="noopener">miRTarBase</a>（实验验证）或 <a href="https://starbase.sysu.edu.cn/" target="_blank" rel="noopener">starBase</a>（CLIP-seq 证据）查证。<strong>有实验支持的靶向关系可信度远高于纯预测。</strong>

**5. 构建 ceRNA 网络**

ceRNA 假设：lncRNA / circRNA 带有与 mRNA 相同的 miRNA 结合位点（MRE），通过"争抢"miRNA 来调节 mRNA。构建时至少应满足：

<ol>
  <li>两者被同一 miRNA 靶向（序列层面）；</li>
  <li>两者表达量<strong>正相关</strong>（表达层面）；</li>
  <li>共享的 MRE 数量足够，且 miRNA 相对不足（剂量层面）。</li>
</ol>

**6. 网络可视化**

把 "miRNA → 靶基因" 与 "lncRNA/circRNA → miRNA" 两组关系整理成边表，导入 Cytoscape，用不同形状区分三类分子。

## 四、结果判读

<ul>
  <li><strong>结构比序列更重要</strong>：一条序列与已知 miRNA 相似但折不出发夹，不能算 miRNA。</li>
  <li><strong>预测结果必然含假阳性</strong>：单个工具预测的靶基因，通常只有一小部分能被实验验证。报告时应写"预测靶基因"，并说明所用工具与阈值。</li>
  <li><strong>多工具交集更稳</strong>：两个以上工具都命中的靶点，优先级高于单工具结果。</li>
  <li><strong>ceRNA 是假说</strong>：共表达 + 共享 MRE 只构成相关性，不等同于调控关系；严谨的结论需要报告基因实验或敲低验证。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>只做序列比对就下结论</strong>：缺少二级结构证据的新 miRNA 很难被认可。</li>
  <li><strong>忽略物种参数</strong>：植物与动物的靶向规则不同（植物多为近乎完全互补的切割，动物多为种子区不完全配对），用错工具会得到大量错误结果。</li>
  <li><strong>把预测当验证</strong>：论文里"靶基因"若只有预测证据，其结论强度远低于带双荧光素酶实验的结果。</li>
  <li><strong>ceRNA 网络过度解读</strong>：把一张包含上百节点的网络图直接解释为调控机制，是该类分析最常见的硬伤。</li>
</ul>

## 六、练习

<ol>
  <li>从 miRBase 下载本物种已知 miRNA 的成熟序列，统计家族数量。</li>
  <li>取一条候选前体序列用 RNAfold 折叠，画出其发夹结构并计算 MFE。</li>
  <li>用 psRNATarget 或 TargetScan 预测靶基因，记录工具、参数与命中数量。</li>
  <li>在 miRTarBase / starBase 中查证其中 2 条关系是否已有实验支持。</li>
  <li>（选做）构建一个小规模 ceRNA 网络并在 Cytoscape 中出图，说明你设定的筛选条件。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://www.mirbase.org/help/nomenclature.shtml" target="_blank" rel="noopener">miRNA 命名规则</a></li>
  <li><a href="https://www.tbi.univie.ac.at/RNA/RNAfold.1.html" target="_blank" rel="noopener">RNAfold 使用说明</a></li>
  <li><a href="https://www.zhaolab.org/psRNATarget/" target="_blank" rel="noopener">psRNATarget</a></li>
  <li><a href="https://mirtarbase.cuhk.edu.cn/" target="_blank" rel="noopener">miRTarBase</a></li>
</ul>
