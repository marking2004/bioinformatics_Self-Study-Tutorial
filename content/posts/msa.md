---
title: "多序列比对与结果可视化"
date: "2026-10-05"
weight: 50
category: "多序列比对"
meta: "序列 · 约 18 分钟"
draft: "false"
summary: "成对比对只看两条序列；多序列比对（MSA）把三条以上同源序列上下对齐，目的是找出跨物种 / 跨家族都保守的列——这些列往往对应功能位点或结构核心。它是系统发育、蛋白家族、基序发现的前提。"
---

<p>成对比对只看两条序列；<strong>多序列比对（MSA）</strong>把三条以上同源序列上下对齐，目的是找出跨物种 / 跨家族都保守的列——这些列往往对应功能位点或结构核心。它是系统发育、蛋白家族、基序发现的前提。</p>
          <h2>1. 一条典型流程</h2>
          <ol>
            <li>收集同源序列：先用模块"序列比对与 BLAST"拿到一批同源蛋白 / 核酸；</li>
            <li>去冗余、统一格式（FASTA）；</li>
            <li>跑 MSA（MAFFT 最快且质量好）；</li>
            <li>修剪低置信区（trimAl）；</li>
            <li>可视化与解读（Jalview、序列 Logo）。</li>
          </ol>
          <h2>2. 在命令行跑 MAFFT</h2>
          <pre><code># --auto 让程序自动选策略；输出比对后的 fasta
mafft --auto seqs.fasta &gt; aln.fasta

# 序列很多时可并行
mafft --auto --thread 8 big.fasta &gt; big_aln.fasta</code></pre>
          <p>替代工具：ClustalOmega（稳）、MUSCLE（快）。在线可用 EMBL-EBI 的 MSA 工具，无需安装。</p>
          <h2>3. 用 Jalview 可视化</h2>
          <p>Jalview 是看 MSA 的标准桌面软件（有 Windows 版）：</p>
          <ul>
            <li>打开 <code>aln.fasta</code> → 颜色按保守度上色；</li>
            <li><strong>Conservation</strong> 视图标出高保守列；</li>
            <li>计算<strong>邻接树</strong>快速看聚类；</li>
            <li>导出 PNG / EPS 用于论文。</li>
          </ul>
          <h2>4. 序列 Logo：把保守性画成图</h2>
          <p>WebLogo 或 ggseqlogo（R）把每列画成字母高度 = 出现频率的"logo"：越高越保守。</p>
          <pre><code># R 里用 ggseqlogo
library(ggseqlogo)
p &lt;- ggseqlogo(sequences, method = "bits")
plot(p)</code></pre>
          <h2>5. 怎么读结果</h2>
          <ul>
            <li><strong>全保守列</strong>：高度可能是活性中心或结合位点；</li>
            <li><strong>成块插入 / 缺失</strong>：常是柔性环区，比对不可靠，谨慎解读；</li>
            <li><strong>半保守（如 K/R 互换）</strong>：功能保留但序列变化。</li>
          </ul>
          <blockquote>MSA 的质量决定下游一切。低相似度的远缘序列强行对齐，会得到"假保守"。比对后一定用眼看一下，别全信软件。</blockquote>


## 迷你实战

把几个同源蛋白对齐，看保守位点（序列由你自己准备，或用"综合实战"第 3 步生成）：

```bash
mafft --auto tp53_orthologs.fasta > aln.fa
```

观察：对齐后各序列长度一致；用 AliView / Jalview 打开，`*` 行表示完全保守列——这些往往对应关键功能位点。
