---
title: "虚拟筛选与计算机辅助药物设计"
date: "2026-10-05"
weight: 120
category: "药物设计"
meta: "药物 · 约 20 分钟"
draft: "false"
summary: "计算机辅助药物设计（CADD）用结构和计算，从海量化合物里挑出'值得合成验证'的少数候选。本模块走一条标准链路：靶点 → 对接 → 筛选 → 性质评估。"
---

<p>计算机辅助药物设计（CADD）用结构和计算，从海量化合物里挑出"值得合成验证"的少数候选。本模块走一条标准链路：靶点 → 对接 → 筛选 → 性质评估。</p>
          <h2>1. 准备靶点结构</h2>
          <ul>
            <li>从 PDB / AlphaFold DB 取蛋白结构，清掉水、加全氢、修侧链（可用 PyMOL / ChimeraX）；</li>
            <li>定义<strong>结合口袋</strong>：已知配体位置、或同源结构、或 SiteMap / fpocket 预测。</li>
          </ul>
          <h2>2. 分子对接（核心）</h2>
          <p>把小分子"摆"进口袋并算结合打分。常用 <strong>AutoDock Vina</strong>（免费、快）：</p>
          <pre><code># 先准备受体/配体为 pdbqt，再对接
vina --receptor rec.pdbqt --ligand lig.pdbqt \
     --config box.txt --out out.pdbqt</code></pre>
          <p>对接打分是"相对排序"不是绝对亲和力；同一蛋白不同软件结果可能不同，要交叉验证。</p>
          <h2>3. 虚拟筛选</h2>
          <p>对大型库（ZINC、PubChem、Enamine）批量对接，取高分候选。注意：先对库做类药性与去重过滤，再筛，省时间。</p>
          <h2>4. ADMET 与类药性</h2>
          <p>结合好不等于能成药。用 <strong>SwissADME</strong> / admetSAR 评估：</p>
          <ul>
            <li><strong>类药五规则（Lipinski）</strong>：分子量、logP、氢键供体/受体数；</li>
            <li><strong>ADMET</strong>：吸收、分布、代谢、排泄、毒性预测；</li>
            <li><strong>水溶性 / 渗透性</strong>：如 ALOGPS、SwissADME 的溶解度预测，与口服吸收相关；</li>
            <li><strong>致敏性（皮肤致敏）</strong>：如 OECD QSAR Toolbox、admetSAR 的致敏性预测，评估接触风险；</li>
            <li><strong>毒性 / 脱靶</strong>：hERG、CYP 抑制等。</li>
          </ul>
          <h2>5. 配体分子结构生成与优化</h2>
          <p>拿到配体（SMILES，或从 ZINC、PubChem 下载）后，需先变成"能对接的 3D 结构"：</p>
          <ul>
            <li><strong>2D → 3D</strong>：用 Open Babel（<code>obabel mol.smi -O mol.pdb --gen3d</code>）、RDKit 生成初始三维构象；</li>
            <li><strong>构象搜索 / 力场优化</strong>：MMFF94（Open Babel / RDKit）、UFF，取低能构象作为对接输入；</li>
            <li><strong>质子化状态 / 互变异构</strong>：用 cxcalc、Open Babel（<code>--p</code>）或 ChemAxon 处理特定 pH 下的主要形态；</li>
            <li><strong>去重与类药性预筛</strong>：同一分子只留一个低能构象，先按类药五规则 / PAINS 过滤再对接。</li>
          </ul>
          <p>少量分子可手画（MarvinSketch、ChemDraw）再转 3D；批量用 RDKit 脚本生成。这一步决定对接"喂进去的构象"合不合理，直接影响打分。</p>
          <h2>6. 先导优化</h2>
          <p>拿到苗头化合物后，用结构指导改取代基、调 pK、改善选择性，循环"设计—合成—测试"。现代也用生成式模型（如 REINVENT）探索化学空间。</p>
          <blockquote>对接只是"过滤"不是"预测"。高分候选仍需湿实验（SPR / 酶活 / 细胞）确认；别把对接打分当 IC50。</blockquote>


## 迷你实战

小分子对接入门：用网页 SwissDock（http://www.swissdock.ch/）上传蛋白 PDB 与配体看结合口袋打分；本地用 AutoDock Vina：

```bash
conda install -c bioconda autodock-vina
vina --receptor receptor.pdbqt --ligand ligand.pdbqt --out out.pdbqt --exhaustiveness 8
```

观察：结果按结合自由能排序，越负越优。想深入设计见"肽与蛋白质合理设计"模块。
