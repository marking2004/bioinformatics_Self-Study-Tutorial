---
title: "实验 8：系统发生树构建与可靠性评估"
date: "2026-10-10"
weight: 80
category: "序列分析"
meta: "序列 · 约 55 分钟"
module: "phylogenetics"
draft: false
summary: "从联配到一棵可发表的树，中间隔着模型选择和支持率评估。本实验用 IQ-TREE 走完完整链路，并说清枝长、支持率和'基因树不等于物种树'这些容易讲错的点。"
---

> 所属模块：[系统发育分析](../posts/phylogenetics.html)

## 一、实验目的

<ul>
  <li>掌握分子系统发生的标准链路：同源序列 → 联配 → 模型选择 → 建树 → 支持率评估；</li>
  <li>理解 <strong>距离法、最大似然（ML）、贝叶斯（BI）</strong>的差异与适用场合；</li>
  <li>会用 IQ-TREE 完成建模与建树，并用 bootstrap 评估分支可信度；</li>
  <li>正确理解枝长、支持率与定根的含义。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>IQ-TREE</td><td>ML 建树 + 自动模型选择</td><td><a href="http://www.iqtree.org/" target="_blank" rel="noopener">iqtree.org</a> · <a href="http://iqtree.cibiv.univie.ac.at/" target="_blank" rel="noopener">在线服务</a></td></tr>
    <tr><td>FastTree</td><td>超快近似 ML，适合大数据快速预览</td><td><a href="http://www.microbesonline.org/fasttree/" target="_blank" rel="noopener">FastTree</a></td></tr>
    <tr><td>MEGA</td><td>图形界面，教学常用</td><td><a href="https://www.megasoftware.net/" target="_blank" rel="noopener">MEGA</a></td></tr>
    <tr><td>FigTree / iTOL</td><td>树的查看与美化</td><td><a href="http://tree.bio.ed.ac.uk/software/figtree/" target="_blank" rel="noopener">FigTree</a> · <a href="https://itol.embl.de/" target="_blank" rel="noopener">iTOL</a></td></tr>
    <tr><td>ggtree（R）</td><td>可编程的树图</td><td><a href="https://yulab-smu.top/treedata-book/" target="_blank" rel="noopener">ggtree 手册</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 输入：修剪过的联配**

<p>直接沿用<a href="msa.html">实验 7</a> 的产物（FASTA 或 PHYLIP 均可）。<strong>联配质量决定树的质量</strong>——这一步偷懒，后面再好的模型也救不回来。</p>

**2. 选择替代模型**

<p>模型描述"一个碱基/氨基酸变成另一个的概率"。模型选错，拓扑和枝长都会偏。IQ-TREE 内置的 <strong>ModelFinder</strong> 会自动比较并挑最优模型：</p>

```bash
iqtree -s aligned.fasta -m TESTONLY          # 只做模型选择
```

输出里 <em>Best-fit model</em> 一行即为推荐模型（如 <code>JTT+F+I+G4</code>）。

**3. 建树 + 支持率评估**

```bash
# 推荐做法：自动模型 + 1000 次超快 bootstrap
iqtree -s aligned.fasta -m MFP -B 1000 -T 4 --prefix mytree

# 快速预览（大数据集）
FastTree -lg aligned.fasta > fasttree.nwk      # 蛋白用 -lg，核酸用 -nt
```

<ul>
  <li><code>-m MFP</code>：ModelFinder Plus，自动选模型再建树；</li>
  <li><code>-B 1000</code>：1000 次 UFBoot（超快 bootstrap），评估每个分支的稳定性；</li>
  <li><code>-T 4</code>：线程数。</li>
</ul>

**4. 指定外群定根**

```bash
iqtree -s aligned.fasta -m MFP -B 1000 -o Outgroup_taxon
```

<p>建树程序输出的树<strong>默认是无根的</strong>。要让树"有方向"，必须指定一个已知较早分化的外群（outgroup）。</p>

**5. 可视化**

<ul>
  <li><strong>FigTree</strong>：打开 <code>.treefile</code>，可显示支持率、给分支上色、导出 PDF/SVG；</li>
  <li><strong>iTOL</strong>：上传树文件，可叠加物种分组、结构域、热图等多层注释，适合做发表级图；</li>
  <li><strong>ggtree</strong>：R 里用代码画图，批量或可重复出图时效率最高。</li>
</ul>

## 四、结果判读

<ul>
  <li><strong>支持率怎么看</strong>：UFBoot 值 ≥ 95 通常认为该分支可信；传统 bootstrap ≥ 70–80 视为基本支持。低于此的分支在论文里应视为"未解决"，不能写成结论。</li>
  <li><strong>枝长代表什么</strong>：默认枝长是<strong>每位点的预期替代数</strong>，不是时间。要讲"多少万年前分化"，必须额外做分子钟标定（如 BEAST、r8s、treePL）。</li>
  <li><strong>基因树 ≠ 物种树</strong>：单个基因的历史可能因不完全谱系分选、水平转移、杂交而与物种历史不一致。严谨的结论通常用多基因串联或共祖方法。</li>
  <li><strong>直系同源 vs 旁系同源</strong>：树里混入了 paralog（基因复制产物）会让拓扑看起来像"物种关系"，实际反映的是复制事件。取样时要区分。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>长枝吸引</strong>：进化快、枝很长的序列容易被错误地聚在一起。换更好的模型（如加 G、加 F）或减少远缘序列可缓解。</li>
  <li><strong>模型不换</strong>：蛋白和核酸模型不能混用；核酸还要区分是否考虑碱基频率与非均一速率。</li>
  <li><strong>拿 NJ 树的结论直接写报告</strong>：距离法快但信息利用不充分，正式结论建议 ML 或 BI。</li>
  <li><strong>序列里混了不同拷贝</strong>：同一物种的多个 isoform 或旁系同源一起建树，会得到看似漂亮实则错误的树。</li>
  <li><strong>只看拓扑不看支持率</strong>：没有支持率的树只是一张图。</li>
</ul>

## 六、练习

<ol>
  <li>用实验 7 的联配结果跑 <code>iqtree -m TESTONLY</code>，记录最优模型名称。</li>
  <li>用 <code>-m MFP -B 1000</code> 建树，统计支持率 ≥95 的分支占比。</li>
  <li>指定一个外群重新建树，比较定根前后的拓扑差异。</li>
  <li>用 FigTree 打开树，标出支持率最低的分支，说明它在生物学上意味着什么。</li>
  <li>（选做）把树上传到 iTOL，叠加物种分组色带并导出图片。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="http://www.iqtree.org/doc/" target="_blank" rel="noopener">IQ-TREE 官方文档</a></li>
  <li><a href="https://itol.embl.de/help.cgi" target="_blank" rel="noopener">iTOL 帮助文档</a></li>
  <li><a href="https://yulab-smu.top/treedata-book/" target="_blank" rel="noopener">ggtree 使用手册</a></li>
  <li><a href="http://evolution.genetics.washington.edu/phylip/" target="_blank" rel="noopener">Phylip 与系统发生方法综述</a></li>
</ul>
