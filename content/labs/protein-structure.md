---
title: "实验 15：蛋白质功能域、结构预测与同源建模"
date: "2026-10-10"
weight: 150
category: "蛋白结构"
meta: "结构 · 约 60 分钟"
module: "protein-analysis"
draft: false
summary: "拿到一条序列，先看它有哪些功能域，再决定用什么方法得到结构。本实验扫功能域、判跨膜与信号肽、用 SWISS-MODEL 与 AlphaFold 建模，并学会看懂质量指标。"
---

> 所属模块：[蛋白质分析](../posts/protein-analysis.html)

## 一、实验目的

<ul>
  <li>用 InterPro 等资源扫描功能域与保守基序，为序列做"身份登记"；</li>
  <li>判定跨膜区与信号肽，避免把膜蛋白当可溶性球蛋白建模；</li>
  <li>会用<strong>同源建模</strong>与 <strong>AlphaFold DB</strong> 两条途径获取结构；</li>
  <li>能读懂 QMEAN、Ramachandran 与 pLDDT，并知道哪些区域不可信。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具 / 数据库</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>InterPro</td><td>功能域与位点整合扫描</td><td><a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a></td></tr>
    <tr><td>Pfam / PROSITE / SMART</td><td>具体域数据库</td><td><a href="https://pfam.xfam.org/" target="_blank" rel="noopener">Pfam</a> · <a href="https://prosite.expasy.org/" target="_blank" rel="noopener">PROSITE</a> · <a href="https://smart.embl.de/" target="_blank" rel="noopener">SMART</a></td></tr>
    <tr><td>TMHMM / SignalP</td><td>跨膜区与信号肽</td><td><a href="https://services.healthtech.dtu.dk/services/TMHMM-2.0/" target="_blank" rel="noopener">TMHMM</a> · <a href="https://services.healthtech.dtu.dk/services/SignalP-6.0/" target="_blank" rel="noopener">SignalP</a></td></tr>
    <tr><td>SWISS-MODEL</td><td>同源建模</td><td><a href="https://swissmodel.expasy.org/" target="_blank" rel="noopener">SWISS-MODEL</a></td></tr>
    <tr><td>AlphaFold DB</td><td>预测结构库</td><td><a href="https://alphafold.ebi.ac.uk/" target="_blank" rel="noopener">AlphaFold DB</a></td></tr>
    <tr><td>PyMOL / ChimeraX</td><td>结构可视化</td><td><a href="https://pymol.org/" target="_blank" rel="noopener">PyMOL</a> · <a href="https://www.cgl.ucsf.edu/chimerax/" target="_blank" rel="noopener">ChimeraX</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 功能域扫描**

把序列提交到 <a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a>，结果会整合 Pfam、PROSITE、SMART、CDD 等多个数据库的命中。重点看：

<ul>
  <li>命中的<strong>结构域名称与位置</strong>（起止残基）；</li>
  <li>关键<strong>活性位点残基</strong>（active site）；</li>
  <li>是否属于某个已知家族。</li>
</ul>

**2. 跨膜区与信号肽**

<p>提交到 <a href="https://services.healthtech.dtu.dk/services/TMHMM-2.0/" target="_blank" rel="noopener">TMHMM 2.0</a> 与 <a href="https://services.healthtech.dtu.dk/services/SignalP-6.0/" target="_blank" rel="noopener">SignalP 6.0</a>。</p>

<ul>
  <li>信号肽通常在 N 端 15–30 个残基，建模前一般要<strong>去掉</strong>；</li>
  <li>跨膜螺旋区域不适合用普通可溶性蛋白的建模流程，需专门处理。</li>
</ul>

**3. 同源建模（SWISS-MODEL）**

提交序列到 SWISS-MODEL，它会自动搜索模板并给出：

<ul>
  <li><strong>模板</strong>（PDB ID）与<strong>序列一致性</strong>；</li>
  <li>GMQE（全局模型质量估计，0–1，越高越好）；</li>
  <li>QMEAN（与高质量实验结构的比较分数）。</li>
</ul>

<p>序列一致性是同源建模的生命线：<strong>&gt;30% 通常可用，&gt;50% 较可靠，&lt;20% 的模型只能看个大概拓扑。</strong></p>

**4. 直接取预测结构**

先查 <a href="https://alphafold.ebi.ac.uk/" target="_blank" rel="noopener">AlphaFold DB</a>：若该蛋白（或近缘物种同源蛋白）已有条目，直接下载 PDB 与对应的<strong>置信度文件（pLDDT）</strong>。

**5. 质量评估**

<ul>
  <li><strong>pLDDT（AlphaFold 每残基置信度）</strong>：&gt;90 高可信（骨架与侧链都较准）；70–90 骨架大致正确；50–70 低可信；<strong>&lt;50 往往是无序区，不应据此做结论</strong>。</li>
  <li><strong>Ramachandran 图</strong>（PROCHECK / MolProbity）： favored 区残基比例越高越好，一般 &gt;98% 才算高质量。</li>
  <li><strong>QMEAN z-score</strong>：接近 0 说明与实验结构质量相当，低于 -4 提示模型有问题。</li>
</ul>

**6. 可视化**

```bash
pymol model.pdb
```

<ul>
  <li>按 pLDDT 着色（AlphaFold 模型常用）：蓝色高置信、橙色/红色低置信；</li>
  <li>用 ChimeraX 的 <code>matchmaker</code> 把预测结构与实验结构叠合，看 RMSD。</li>
</ul>

## 四、结果判读

<ul>
  <li><strong>先看功能域再看结构</strong>：功能域告诉你"它可能干什么"，结构告诉你"它长什么样"，两者结合才能设计突变或解释表型。</li>
  <li><strong>局部置信度比全局分数重要</strong>：整体 pLDDT 80 的模型，若活性位点恰好落在 50 的区域，这个模型就不能用于机制推断。</li>
  <li><strong>预测结构不等于实验结构</strong>：AlphaFold 给的是单一静态构象，缺少配体、辅因子、金属离子与构象变化信息。</li>
  <li><strong>缺失区段是常态</strong>：长插入环、无序尾常无法建模，图上表现为"断链"或空白，不要误认为结构特殊。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>拿一条片段去建模</strong>：只提交结构域序列会丢失上下文，最好用全长序列建模后再截取。</li>
  <li><strong>忽略寡聚状态</strong>：单体模型无法解释界面突变，功能形式若是二聚体需另做组装（如用同源模板的对称信息）。</li>
  <li><strong>把低置信区写进结论</strong>：pLDDT &lt;50 或模板一致性 &lt;20% 的区域，只能作为参考。</li>
  <li><strong>不检查模板是否被配体/其他链污染</strong>：模板若来自复合物，模型可能继承了结合构象。</li>
</ul>

## 六、练习

<ol>
  <li>对一个未知功能的蛋白序列跑 InterPro，列出命中的结构域、位置与所属家族。</li>
  <li>用 TMHMM 与 SignalP 判断它是否有跨膜区或信号肽。</li>
  <li>在 SWISS-MODEL 建模，记录模板 PDB、序列一致性、GMQE 与 QMEAN。</li>
  <li>在 AlphaFold DB 查找同一蛋白，下载 PDB 并用 PyMOL 按 pLDDT 着色。</li>
  <li>（选做）对比两种方法得到的结构，用 ChimeraX 叠合，报告 RMSD 与主要差异区域。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a></li>
  <li><a href="https://swissmodel.expasy.org/docs/help" target="_blank" rel="noopener">SWISS-MODEL 帮助文档</a></li>
  <li><a href="https://alphafold.ebi.ac.uk/faq" target="_blank" rel="noopener">AlphaFold DB FAQ（含 pLDDT 说明）</a></li>
  <li><a href="https://www.cgl.ucsf.edu/chimerax/docs/user/index.html" target="_blank" rel="noopener">ChimeraX 用户手册</a></li>
</ul>
