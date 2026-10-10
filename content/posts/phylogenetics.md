---
title: "系统发育分析：单基因 / 多基因 / 组学"
date: "2026-10-05"
weight: 100
category: "系统发育"
meta: "进化 · 约 20 分钟"
draft: "false"
summary: "系统发育回答'谁和谁更近'。但'近'取决于你用哪段证据——一个基因、多个基因，还是全基因组。本模块按证据层次递进。"
---

<p>系统发育回答"谁和谁更近"。但"近"取决于你用哪段证据——一个基因、多个基因，还是全基因组。本模块按证据层次递进。</p>
          <h2>1. 单基因树（最常见的入门）</h2>
          <p>流程：多序列比对（见 MSA 模块）→ 修剪（trimAl）→ 选替换模型 → 建树 → 自举检验。</p>
          <pre><code># IQ-TREE：自动选模型 + 1000 次自举
iqtree2 -s aln.trim.fasta -m MFP -B 1000 -T 4</code></pre>
          <ul>
            <li><strong>建树法</strong>：邻接法（快）、最大似然（ML，准）、贝叶斯（慢但给后验概率）；</li>
            <li><strong>自举（bootstrap）</strong>：重复抽样看节点稳不稳，&gt;70% 一般可信；</li>
            <li><strong>定根</strong>：用外类群（outgroup）确定进化方向。</li>
          </ul>
          <h2>2. 多基因联合</h2>
          <p>单基因可能因不完全谱系分选（ILS）而"说谎"。两种策略：</p>
          <ul>
            <li><strong>串联法</strong>：把多个基因比对拼接成超级矩阵，一起建 ML 树（简单但假设无冲突）；</li>
            <li><strong>聚合法（推荐）</strong>：每个基因先建树，再用 <strong>ASTRAL</strong> / *BEAST 聚合为物种树，能处理 ILS。</li>
          </ul>
          <h2>3. 基于组学数据</h2>
          <ul>
            <li><strong>系统发育剖面</strong>：以"基因在各物种有无"做距离，推断功能关联；</li>
            <li><strong>直系同源矩阵</strong>：用 OrthoFinder 得到同源组，构建种间关系；</li>
            <li><strong>SNP / 变异矩阵</strong>：群体重测序可直接做系统发育（见基因组学模块）。</li>
          </ul>
          <h2>4. 读树时要小心</h2>
          <blockquote>长枝吸引（LBA）：两个快速进化的长枝会被错误地拉到一起。加外类群、用不同模型、看自举，都能帮忙发现它。</blockquote>
          <p>树的"枝长"是变化量，"节点支持率"才是可信度——别把长得好看的树当成对的树。</p>


## 迷你实战

基于"综合实战"第 4 步的对齐建树；想自己准备数据也行：

```bash
iqtree2 -s aln.fa -m MFP -bb 1000 -nt AUTO
```

观察：`.treefile` 是 Newick 格式；上传到 iTOL 网页即可出图。多基因联合只需把多个对齐 Concatenate 后一起建树（这是"基于多基因"的一层）。
