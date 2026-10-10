---
title: "肽与蛋白质设计：合理设计与从头设计"
date: "2026-10-05"
weight: 90
category: "蛋白质设计"
meta: "蛋白质 · 约 20 分钟"
draft: "false"
summary: "分析是'读懂'蛋白质，设计是'写'蛋白质。本模块覆盖两类思路：在天然骨架上改（合理设计 / 定向进化），以及从零生成新骨架（从头设计）。肽设计是其中更轻量、更贴近抗菌 / 结合应用的入口。"
---

<p>分析是"读懂"蛋白质，设计是"写"蛋白质。本模块覆盖两类思路：在天然骨架上改（合理设计 / 定向进化），以及从零生成新骨架（从头设计）。肽设计是其中更轻量、更贴近抗菌 / 结合应用的入口。</p>
          <h2>1. 合理设计（基于结构与机理）</h2>
          <ul>
            <li><strong>定点突变</strong>：改关键残基调活性、稳定性或特异性（如把 Ser 换成 Cys 加二硫键）；</li>
            <li><strong>共识设计</strong>：参考一个家族的多序列比对，取"最共识"残基提高热稳定性；</li>
            <li><strong>酶工程</strong>：用结构 + 分子动力学（MD）评估突变效果。</li>
          </ul>
          <h2>2. 定向进化（"无理性"但有效）</h2>
          <p>不依赖结构知识：易错 PCR 引入随机突变 → 建库 → 筛选 / 选择（噬菌体展示、酵母展示）→ 多轮富集。适合"说不清机理但要有功能"的场景。</p>
          <h2>3. 从头设计（de novo）</h2>
          <p>近年 AI 让"凭空设计"成为现实，核心三步循环：</p>
          <ol>
            <li><strong>骨架生成</strong>：RFdiffusion / Chroma 生成满足约束的新折叠；</li>
            <li><strong>序列设计</strong>：ProteinMPNN 在给定骨架上设计氨基酸序列；</li>
            <li><strong>过滤与预测</strong>：用 AlphaFold 重预测，挑 pLDDT 高、自洽性好的候选。</li>
          </ol>
          <pre><code># RFdiffusion 生成结合某表位的 scaffold
python run_inference.py --pmpnn True \
  --contig 'B15-25/0 0 25-35' --out_dir designs/</code></pre>
          <h2>4. 肽设计专门路径</h2>
          <ul>
            <li><strong>抗菌肽（AMP）</strong>：看疏水性、正电荷、两亲性螺旋；</li>
            <li><strong>结合肽 / 抑制剂</strong>：可来自噬菌体展示淘选，或用 RFdiffusion 的 binder 模式；</li>
            <li><strong>工具</strong>：PeptideBuilder、HeliQuest、CAMPR4（AMP 数据库与预测）。</li>
          </ul>
          <h2>5. 一条可落地的流程</h2>
          <p>明确功能目标 → 选骨架（天然改 / 从头生成）→ 设计序列 → <em>in silico</em> 检验（折叠自洽、对接、ADMET）→ 合成与实验验证。</p>
          <blockquote>设计比分析更"软"：计算上"很漂亮"的蛋白，湿实验可能不表达、不折叠。务必准备多候选、并行验证，别把宝押在一个序列上。</blockquote>


## 迷你实战

一窥从头设计：先用 AlphaFold 预测你关心的蛋白结构（结构可直接从 AFDB 下载，见"综合实战"第 5 步）：

```bash
curl -s "https://alphafold.ebi.ac.uk/files/AF-P04637-F1-model_v4.cif" -o P04637.cif
```

观察：结构文件用 PyMOL / ChimeraX 打开；想真正设计新蛋白再回到 RFdiffusion / ProteinMPNN 流程（需 GPU 或 Colab）。
