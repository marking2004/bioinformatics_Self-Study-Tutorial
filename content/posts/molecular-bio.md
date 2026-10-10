---
title: "分子生物学实验：引物、载体与 CRISPR"
date: "2026-10-05"
weight: 20
category: "分子生物学"
meta: "实验 · 约 18 分钟"
draft: "false"
summary: "生信不只服务计算，也直接服务于 bench。这一模块讲三件'下机前先算一遍'的事，能省大量试错成本。"
---

<p>生信不只服务计算，也直接服务于 bench。这一模块讲三件"下机前先算一遍"的事，能省大量试错成本。</p>
          <h2>1. 引物设计</h2>
          <ul>
            <li><strong>PCR 引物</strong>：用 NCBI Primer-BLAST 或 Primer3；目标 Tm 接近（差 &lt;5℃）、长度 18–25 nt、GC 40–60%、产物 100–500 bp；</li>
            <li><strong>避免</strong>：自身 / 引物间二聚体、发夹、3′ 端互补；</li>
            <li><strong>特异性</strong>：在基因组里 BLAST 确认只扩目标区域。</li>
          </ul>
          <pre><code># Primer3 也可命令行调用（pyPCR 等封装）
primer3_core --input input_seq.txt --output primers.txt</code></pre>
          <h2>2. 载体构建</h2>
          <ul>
            <li><strong>限制性酶切 + 连接</strong>：经典但受酶切位点限制；</li>
            <li><strong>Gibson / Golden Gate</strong>：无缝组装多个片段，Golden Gate 用 Type IIs 酶可一次性组装；</li>
            <li><strong>工具</strong>：SnapGene / Benchling 做图谱与引物规划（含Windows 本地版）。</li>
          </ul>
          <h2>3. CRISPR 靶点设计与脱靶</h2>
          <ol>
            <li>选靶点：用 <strong>CRISPOR</strong> / <strong>CHOPCHOP</strong> 在编码区 early exon 找 20 nt 原间隔序列（PAM 如 NGG）；</li>
            <li>评分：看 on-target 效率（如 CRISPOR 的 Doench 评分）；</li>
            <li>脱靶：用 <strong>Cas-OFFinder</strong> / CasFinder 在全基因组搜近同源位点，挑脱靶少的；</li>
            <li>验证：T7E1 / Sanger 或深度测序看编辑效率。</li>
          </ol>
          <blockquote>湿实验的"算"很便宜，"做"很贵。引物二聚体、载体反向连、CRISPR 脱靶——这些在电脑上花十分钟能避开的坑，在实验台上要花一周重做。</blockquote>


## 迷你实战

设计一对 PCR 引物：用在线 Primer3（https://primer3.ut.ee/）或 NCBI Primer-BLAST（https://www.ncbi.nlm.nih.gov/tools/primer-blast/），粘贴目标序列即拿到引物与 Tm。

观察：好引物一般 18–25 nt、Tm≈55–65℃、无显著二聚体/发夹。本地可用 `primer3-py` 批量设计。
