---
title: "实验 18：Cytoscape 网络构建与分析"
date: "2026-10-10"
weight: 180
category: "网络分析"
meta: "网络 · 约 50 分钟"
module: "multi-omics"
draft: false
summary: "前面各实验得到的基因、蛋白与互作关系，最后都要落到一张网络上。本实验用 Cytoscape 建网、做拓扑分析、找模块与枢纽节点，并给出可用于报告的出图规范。"
---

> 所属模块：[多组学整合分析](../posts/multi-omics.html)

## 一、实验目的

<ul>
  <li>理解网络的基本语言：节点、边、度、中心性与模块；</li>
  <li>能从 STRING 或自建边表构建网络，并把表达量等属性映射到图上；</li>
  <li>会用 NetworkAnalyzer、MCODE、cytoHubba 做拓扑与模块分析；</li>
  <li>能导出符合投稿要求的图片，并理解网络结论的边界。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具 / 数据库</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>Cytoscape</td><td>网络分析与可视化平台</td><td><a href="https://cytoscape.org/" target="_blank" rel="noopener">cytoscape.org</a></td></tr>
    <tr><td>STRING</td><td>蛋白互作（PPI）来源</td><td><a href="https://string-db.org/" target="_blank" rel="noopener">STRING</a></td></tr>
    <tr><td>BioGRID / GeneMANIA</td><td>互作与功能关联</td><td><a href="https://thebiogrid.org/" target="_blank" rel="noopener">BioGRID</a> · <a href="https://genemania.org/" target="_blank" rel="noopener">GeneMANIA</a></td></tr>
    <tr><td>MCODE / cytoHubba</td><td>模块识别与枢纽节点</td><td>Cytoscape App Store 内安装</td></tr>
    <tr><td>ClueGO / EnrichmentMap</td><td>网络上的功能富集</td><td>Cytoscape App Store 内安装</td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 准备数据**

两种方式：

<ul>
  <li><strong>从 STRING 直接建网</strong>：在 STRING 输入基因列表（如差异基因），设定置信度阈值，导出 TSV 或直接通过 <em>stringApp</em> 在 Cytoscape 内导入；</li>
  <li><strong>自建边表</strong>：准备两列（source / target）的 CSV，例如 miRNA–靶基因、lncRNA–miRNA 关系。</li>
</ul>

**2. 导入网络**

<em>File → Import → Network from File</em> 选择边表；<em>File → Import → Table from File</em> 导入节点属性（如 log2FC、padj、模块归属）。

**3. 映射视觉样式**

在左侧 <em>Style</em> 面板：

<ul>
  <li><strong>节点颜色</strong>映射到 log2FC（红=上调、蓝=下调，或按你的配色规范）；</li>
  <li><strong>节点大小</strong>映射到度（degree）或显著性；</li>
  <li><strong>边粗细/透明度</strong>映射到互作置信度（如 STRING score）。</li>
</ul>

**4. 布局**

常用 <em>Layout → Prefuse Force Directed Layout</em>（力导向，按连接关系自然聚拢）。节点多时先做布局再分析，避免"看不出结构"。

**5. 拓扑分析**

<em>Tools → NetworkAnalyzer → Network Analysis → Analyze Network</em>，输出：

<ul>
  <li><strong>Degree（度）</strong>：一个节点连了多少条边，最直观的"重要性"指标；</li>
  <li><strong>Betweenness（介数中心性）</strong>：多少最短路径经过它，高者常是"桥梁"节点；</li>
  <li><strong>Clustering coefficient</strong>：邻居之间的连接紧密程度。</li>
</ul>

**6. 找模块与枢纽基因**

<ul>
  <li><strong>MCODE</strong>：<em>Apps → MCODE</em>，识别连接密集的子网络（模块），常用于从大网里挑出功能模块；</li>
  <li><strong>cytoHubba</strong>：按 MCC、Degree、EPC 等多种算法排序枢纽基因，取前 10–20 个作为候选。</li>
</ul>

**7. 功能注释**

<em>Apps → ClueGO</em> 对每个模块做 GO / KEGG 富集；或用 <em>EnrichmentMap</em> 把富集结果本身画成网络（节点是通路，边是共享基因）。

**8. 导出图片**

<em>File → Export → Network to Image</em>，选择 PDF 或 SVG（矢量），分辨率设 300 dpi 以上。避免直接截图。

## 四、结果判读

<ul>
  <li><strong>度分布</strong>：生物网络常近似无标度——少数节点度很高（hub），多数节点度很低。若你的网络度分布均匀，多半是数据来源或阈值有问题。</li>
  <li><strong>STRING 置信度阈值的含义</strong>：中等置信度一般取 0.4，高置信度取 0.7。阈值越高边越少越可靠，但也越容易漏掉真实互作。报告中必须写明所用阈值。</li>
  <li><strong>枢纽基因是候选</strong>：高 degree 只说明它在现有数据里连接多，可能受"研究热度偏差"影响（研究多的基因互作记录也多）。</li>
  <li><strong>网络展示的是关联，不是因果</strong>：一条边表示"有报道的互作/共表达"，不能直接推出调控方向与强度。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>节点太多导致"毛球图"</strong>：上千节点无布局的网络图没有信息量。先按 degree 或显著性筛选，再展示核心子网。</li>
  <li><strong>ID 不匹配</strong>：属性表与网络的节点 ID 必须完全一致（大小写、版本号），否则属性映射不上。</li>
  <li><strong>阈值不写明</strong>：同一组基因用 0.4 与 0.7 会得到完全不同的网络，不写阈值的结果无法复现。</li>
  <li><strong>把 PPI 网络当调控网络</strong>：蛋白互作不等于一个调控另一个，方向性需要额外数据支撑。</li>
  <li><strong>图片用位图截图</strong>：投稿会被要求重画。养成导出 PDF/SVG 的习惯。</li>
</ul>

## 六、练习

<ol>
  <li>取一组差异基因（20–50 个）导入 STRING，分别用 0.4 与 0.7 两个阈值建网，比较边数。</li>
  <li>把 log2FC 映射到节点颜色，度映射到节点大小，导出一张图。</li>
  <li>用 NetworkAnalyzer 输出度分布，指出度最高的 5 个节点。</li>
  <li>用 MCODE 找出模块，对最大模块做 GO 富集并说明其可能的生物学含义。</li>
  <li>（选做）用 cytoHubba 的 MCC 算法取前 10 个枢纽基因，与度排序的结果对比是否一致。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://cytoscape.org/documentation_users.html" target="_blank" rel="noopener">Cytoscape 官方文档</a></li>
  <li><a href="https://string-db.org/cgi/help" target="_blank" rel="noopener">STRING 帮助</a></li>
  <li><a href="https://apps.cytoscape.org/apps/mcode" target="_blank" rel="noopener">MCODE 说明</a></li>
  <li><a href="https://apps.cytoscape.org/apps/cytohubba" target="_blank" rel="noopener">cytoHubba 说明</a></li>
</ul>
