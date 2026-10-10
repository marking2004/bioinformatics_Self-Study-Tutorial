---
title: "蛋白质序列分析、结构与功能预测"
date: "2026-10-05"
weight: 80
category: "蛋白质"
meta: "蛋白质 · 约 22 分钟"
draft: "false"
summary: "拿到一条氨基酸序列，能从它身上读出很多事：理化性质、结构、结构域、功能。这一模块把'从序列到结构到功能'的常规路线走一遍。"
---

<p>拿到一条氨基酸序列，能从它身上读出很多事：理化性质、结构、结构域、功能。这一模块把"从序列到结构到功能"的常规路线走一遍。</p>
          <h2>1. 一级性质：先量一量</h2>
          <p>用 Expasy ProtParam 或本地脚本算分子量、等电点（pI）、不稳定指数、半衰期、疏水性等。推测亚细胞定位可看信号肽（SignalP）和跨膜区（TMHMM / DeepTMHMM）。</p>
          <pre><code># 用 Biopython 快速算基础性质
from Bio.SeqUtils.ProtParam import ProteinAnalysis
a = ProteinAnalysis("MKVLT...")
print(a.molecular_weight(), a.isoelectric_point())</code></pre>
          <h2>2. 结构域与家族注释</h2>
          <ul>
            <li><strong>InterPro / Pfam</strong>：扫描已知结构域、重复序列、家族；</li>
            <li><strong>CDD（NCBI）</strong>：保守结构域数据库；</li>
            <li><strong>PROSITE</strong>：特征基序（如活性位点模式）。</li>
          </ul>
          <p>知道结构域，就大致知道它"属于哪一类蛋白、可能干什么"。</p>
          <h2>3. 结构预测（重点：AlphaFold）</h2>
          <p>过去靠同源建模（SWISS-MODEL），如今 <strong>AlphaFold2 / AlphaFold3</strong> 直接从序列预测三维结构，精度接近实验。最省事：直接去 <strong>AlphaFold DB</strong> 搜 UniProt ID 下载结构；本地可用 <strong>ColabFold</strong>。</p>
          <pre><code># ColabFold 本地预测（需 GPU 体验更佳）
colabfold_batch seqs.fasta output_dir/</code></pre>
          <p>读结构时看两个指标：<strong>pLDDT</strong>（单残基置信度，&gt;70 较可靠）和 <strong>PAE</strong>（残基间误差，判断结构域相对位置是否可信）。</p>
          <h2>4. 结构可视化</h2>
          <ul>
            <li><strong>PyMOL</strong>：常用，脚本化上色、量距离、做图；</li>
            <li><strong>UCSF ChimeraX</strong>：免费、对大复合物友好；</li>
            <li><strong>在线</strong>：Mol*（PDB 默认查看器）。</li>
          </ul>
          <h2>5. 功能注释</h2>
          <p>结合 UniProt（功能描述、GO 术语）、KEGG（通路）、STRING（蛋白互作网络）做综合判断。注意：自动注释常只基于同源，关键结论要用实验验证。</p>
          <blockquote>序列 → 结构 → 功能，是一条"越往后越不确定"的链。结构预测很准，但"有结构"不等于"知道功能"；功能注释尤其要保守地下结论。</blockquote>


## 迷你实战

用 Biopython 解析一个蛋白序列并算分子量；结构域注释去 NCBI CDD 或 InterPro 网页上传该序列。

```python
from Bio.Seq import Seq
from Bio.SeqUtils import molecular_weight
seq = Seq("MSK")          # 换成真实序列
print(molecular_weight(seq, "protein"))
```

观察：分子量单位 Da；结构域（如锌指、激酶）通常对应特定功能，是注释的切入点。
