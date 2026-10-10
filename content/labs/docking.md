---
title: "实验 16：分子对接与结合模式分析"
date: "2026-10-10"
weight: 160
category: "药物设计"
meta: "药物 · 约 60 分钟"
module: "cadd"
draft: false
summary: "对接回答'这个小分子能不能塞进这个口袋、怎么塞'。本实验走完受体与配体准备、口袋定义、Vina 对接与结果分析，并强调打分函数能做什么、不能做什么。"
---

> 所属模块：[虚拟筛选与计算机辅助药物设计](../posts/cadd.html)

## 一、实验目的

<ul>
  <li>理解对接的两个核心：<strong>构象搜索</strong>与<strong>打分函数</strong>；</li>
  <li>会准备受体（清理、加氢、定口袋）与配体（3D 结构、质子化、电荷）；</li>
  <li>用 AutoDock Vina 完成一次对接，并分析结合模式与关键相互作用；</li>
  <li>理解打分值的局限，以及"重对接验证"的必要性。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具 / 数据库</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>AutoDock Vina</td><td>主流开源对接程序</td><td><a href="https://vina.scripps.edu/" target="_blank" rel="noopener">vina.scripps.edu</a> · <a href="https://github.com/ccsb-scripps/AutoDock-Vina" target="_blank" rel="noopener">GitHub</a></td></tr>
    <tr><td>MGLTools / ADFR</td><td>受体配体格式转换</td><td><a href="https://ccsb.scripps.edu/mgltools/" target="_blank" rel="noopener">MGLTools</a></td></tr>
    <tr><td>CB-Dock2</td><td>在线自动口袋预测与对接</td><td><a href="https://cadd.labshare.cn/cb-dock2/" target="_blank" rel="noopener">CB-Dock2</a></td></tr>
    <tr><td>PubChem / ZINC</td><td>小分子结构来源</td><td><a href="https://pubchem.ncbi.nlm.nih.gov/" target="_blank" rel="noopener">PubChem</a> · <a href="https://zinc.docking.org/" target="_blank" rel="noopener">ZINC</a></td></tr>
    <tr><td>PyMOL / PLIP</td><td>可视化与相互作用分析</td><td><a href="https://pymol.org/" target="_blank" rel="noopener">PyMOL</a> · <a href="https://plip-tool.biotec.tu-dresden.de/" target="_blank" rel="noopener">PLIP</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 准备受体**

从 <a href="https://www.rcsb.org/" target="_blank" rel="noopener">RCSB PDB</a> 下载结构，然后清理：

<ul>
  <li>去除水分子（除非某个水分子参与催化，需保留）；</li>
  <li>去除共结晶的原有配体与无关链；</li>
  <li>加氢、分配电荷，保存为 PDBQT。</li>
</ul>

```bash
# 用 MGLTools 的 prepare_receptor4.py 转换
prepare_receptor4.py -r receptor.pdb -o receptor.pdbqt -A hydrogens
```

> <strong>金属离子与辅因子</strong>常被忽略：若活性中心含 Zn²⁺、Mg²⁺ 或血红素，删掉它们会让对接结果完全失真。

**2. 准备配体**

<ul>
  <li>从 PubChem 或 ZINC 下载 3D 结构（SDF）；</li>
  <li>确认<strong>质子化状态与互变异构</strong>（生理 pH 下的形式）；</li>
  <li>转成 PDBQT 并定义可旋转键。</li>
</ul>

```bash
obabel -isdf ligand.sdf -opdb -O ligand.pdb --gen3d
prepare_ligand4.py -l ligand.pdb -o ligand.pdbqt
```

**3. 定义对接盒子**

三种方式，优先级从高到低：

<ol>
  <li>用共结晶配体的位置确定口袋中心（最可靠）；</li>
  <li>用文献报道的催化残基坐标；</li>
  <li>用 CB-Dock2 等工具自动预测口袋。</li>
</ol>

盒子一般设为能容纳配体自由旋转的边长（20–25 Å 起步）；太小会限制构象，太大会显著降低精度与速度。

**4. 运行对接**

```bash
vina --receptor receptor.pdbqt --ligand ligand.pdbqt \
     --center_x 10.5 --center_y 22.0 --center_z -5.0 \
     --size_x 22 --size_y 22 --size_z 22 \
     --exhaustiveness 16 --num_modes 9 --energy_range 3 \
     --out out.pdbqt --log log.txt
```

**5. 分析结果**

<ul>
  <li>看结合能排序与构象聚类（是否多个结果收敛到同一姿态）；</li>
  <li>用 PLIP 列出氢键、疏水作用、π-堆积与卤键；</li>
  <li>在 PyMOL 中查看，确认关键残基与文献/突变数据是否吻合。</li>
</ul>

**6. 重对接验证（redocking）**

把共结晶配体重新对接回原口袋，计算其预测姿态与晶体姿态的 <strong>RMSD</strong>。

<p>RMSD &lt; 2 Å 通常说明这套受体准备与盒子参数是合理的；若明显偏大，先修参数，再谈筛选。</p>

## 四、结果判读

<ul>
  <li><strong>结合能只是排序工具</strong>：Vina 给出一个相对的打分（kcal/mol）。文献里常以 &lt;-7 或 &lt;-8 作为"看起来不错"的参考，但<strong>它不等于真实的结合亲和力</strong>，跨体系比较意义有限。</li>
  <li><strong>看一致性而非最优值</strong>：若前 3–5 个构象几乎重合，可信度较高；若每个构象都不同，说明结合模式不确定。</li>
  <li><strong>相互作用要有生物学依据</strong>：与已知催化残基或保守残基形成氢键/疏水接触，比单纯打分低更有说服力。</li>
  <li><strong>打分高不等于有活性</strong>：对接是虚拟筛选的第一道筛子，后续还需类药性过滤与实验验证。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>受体没清理干净</strong>：残留的共结晶配体会占据口袋，导致新配体被挤到别处。</li>
  <li><strong>质子化状态错误</strong>：组氨酸的质子化形式（HID/HIE/HIP）直接影响氢键网络。</li>
  <li><strong>盒子太大或太小</strong>：太大会让配体跑到蛋白表面，太小则限制构象。</li>
  <li><strong>忽略蛋白柔性</strong>：标准 Vina 把受体当作刚性，诱导契合明显的体系需要柔性对接或分子动力学。</li>
  <li><strong>拿对接解释动力学</strong>：对接给的是一个静态快照，不能说明结合/解离速率。</li>
</ul>

## 六、练习

<ol>
  <li>下载一个含共结晶配体的蛋白-配体复合物，写出 PDB ID 与分辨率。</li>
  <li>清理受体并加氢，记录你删除了哪些成分及理由。</li>
  <li>把共结晶配体重新对接回口袋，计算 RMSD 并判断参数是否合理。</li>
  <li>换一个来自 PubChem 的小分子对接，报告其结合能与主要相互作用残基。</li>
  <li>（选做）用 PLIP 输出相互作用表，与文献报道的关键残基对照。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://vina.scripps.edu/manual/" target="_blank" rel="noopener">AutoDock Vina 手册</a></li>
  <li><a href="https://cadd.labshare.cn/cb-dock2/" target="_blank" rel="noopener">CB-Dock2 在线对接</a></li>
  <li><a href="https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index" target="_blank" rel="noopener">PLIP 在线分析</a></li>
  <li><a href="https://www.rcsb.org/docs/general-help/ligands-in-the-pdb" target="_blank" rel="noopener">RCSB 配体说明</a></li>
</ul>
