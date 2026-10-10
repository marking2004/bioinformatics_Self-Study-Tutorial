---
title: "生信软件推荐"
date: "2026-10-05"
weight: 130
category: "软件工具"
meta: "资源 · 约 15 分钟"
draft: "false"
summary: "工具太多反而让人无从下手。这里按'先装什么、各做什么'给一份务实清单，并特别标出 Windows 下能直接用的本地图形工具。"
---

<p>工具太多反而让人无从下手。这里按"在线平台 / 本地图形 / 命令行"分类给一份务实清单，并特别标出 Windows 下能直接用的本地图形工具与国内外在线平台。</p>
          <h2>1. 先装好的"基础环境"</h2>
          <ul>
            <li><strong>WSL2（Windows）</strong>：在 Windows 上跑 Linux 命令行，绝大多数生信工具的家；</li>
            <li><strong>R + RStudio</strong>：统计与可视化（DESeq2、ggplot2、clusterProfiler）；</li>
            <li><strong>Python + (Ana)Conda</strong>：Biopython、各类流程；用 conda 管依赖最省心；</li>
            <li><strong>Git</strong>：取代码、管理版本。</li>
          </ul>
          <h2>2. 在线工具（免安装，浏览器即用）</h2>
          <p>不用装环境、打开网页就能跑，适合临时查一下或教学演示：</p>
          <table>
            <thead><tr><th>工具</th><th>用途</th><th>备注 / 链接</th></tr></thead>
            <tbody>
              <tr><td>NCBI BLAST</td><td>序列比对 / 同源搜索</td><td><a href="https://blast.ncbi.nlm.nih.gov/Blast.cgi" target="_blank" rel="noopener">blast.ncbi.nlm.nih.gov</a></td></tr>
              <tr><td>NCBI COBALT</td><td>多条蛋白 / 核酸的保守域比对</td><td><a href="https://www.ncbi.nlm.nih.gov/tools/cobalt/" target="_blank" rel="noopener">ncbi.nlm.nih.gov/tools/cobalt</a></td></tr>
              <tr><td>NCBI CDD</td><td>保守结构域注释（RPS-BLAST）</td><td><a href="https://www.ncbi.nlm.nih.gov/Structure/cdd/wrpsb.cgi" target="_blank" rel="noopener">ncbi.nlm.nih.gov/Structure/cdd</a></td></tr>
              <tr><td>NCBI ORF Finder</td><td>预测开放阅读框 / 编码区</td><td><a href="https://www.ncbi.nlm.nih.gov/orffinder/" target="_blank" rel="noopener">ncbi.nlm.nih.gov/orffinder</a></td></tr>
              <tr><td>MAFFT 在线（日本 CBRC）</td><td>多序列比对</td><td><a href="https://mafft.cbrc.jp/alignment/server/" target="_blank" rel="noopener">mafft.cbrc.jp/alignment/server</a></td></tr>
              <tr><td>IQ-TREE web</td><td>进化树构建（最大似然）</td><td><a href="https://iqtree.h-its.org/" target="_blank" rel="noopener">iqtree.h-its.org</a></td></tr>
              <tr><td>iTOL</td><td>进化树可视化与注释</td><td><a href="https://itol.embl.de/" target="_blank" rel="noopener">itol.embl.de</a></td></tr>
              <tr><td>BIOPEP-UWM</td><td>肽生物活性预测（波兰 Wrocław 大学）</td><td><a href="https://www.uwm.edu.pl/biochemia/index.php/en/tools/biopp" target="_blank" rel="noopener">uwm.edu.pl/biochemia</a></td></tr>
            </tbody>
          </table>
          <h2>3. Windows 下可直接用的本地图形工具</h2>
          <table>
            <thead><tr><th>工具</th><th>用途</th><th>备注</th></tr></thead>
            <tbody>
              <tr><td>UGENE</td><td>比对 / 进化树 / 可视化一体化</td><td>免费，开箱即用</td></tr>
              <tr><td>Jalview</td><td>多序列比对可视化</td><td>Java，跨平台</td></tr>
              <tr><td>MEGA</td><td>进化树（点选式）</td><td>教学友好</td></tr>
              <tr><td>Benchling</td><td>引物 / 载体 / 实验记录（网页）</td><td>免费版够用</td></tr>
              <tr><td>Cytoscape</td><td>互作网络可视化</td><td>免费</td></tr>
              <tr><td>FigTree / TreeView</td><td>进化树查看</td><td>轻量</td></tr>
              <tr><td>PyMOL</td><td>蛋白结构</td><td>教育版免费</td></tr>
              <tr><td>BioEdit</td><td>序列编辑 / 比对查看（经典老牌）</td><td>Windows，轻量，已多年不更新</td></tr>
              <tr><td>DNAMAN</td><td>序列分析一体化（老牌）</td><td>Windows，教学常用</td></tr>
              <tr><td>DNAStar（Lasergene）</td><td>综合序列分析套件（老牌）</td><td>Windows，商业授权</td></tr>
              <tr><td>SnapGene</td><td>分子克隆 / 质粒图谱</td><td>分子生物学常用，商业授权</td></tr>
              <tr><td>TBtools</td><td>组学数据分析 / 作图一体化（陈程坚等开发）</td><td>国产免费，近年流行</td></tr>
              <tr><td>PhyloSuite</td><td>系统发育分析流水线（张东等开发）</td><td>国产免费，集成多工具</td></tr>
            </tbody>
          </table>
          <p>付费但常用的还有 Geneious（综合）、CLC Genomics（流程）。预算有限可先用免费替代 + 命令行；BioEdit / DNAMAN / DNAStar 等较古早，如今多被免费工具或命令行取代，但老文献与教学中仍常见。</p>
          <h2>4. 命令行主力（各模块对应）</h2>
          <ul>
            <li>比对：BLAST、BWA、minimap2、HISAT2；</li>
            <li>多序列比对：MAFFT、ClustalOmega、MUSCLE；</li>
            <li>进化：IQ-TREE、RAxML、ASTRAL；</li>
            <li>组学：fastp、fastqc、featureCounts、GATK、vcftools；</li>
            <li>药物：AutoDock Vina、Open Babel。</li>
          </ul>
          <h2>5. 选型建议</h2>
          <ul>
            <li>新手先学 <strong>1 个图形工具 + 1 门语言（R 或 Python）</strong>，别贪多；</li>
            <li>同一个分析多软件结果可能不同，重要结论交叉验证；</li>
            <li>优先用 conda / 容器装，避免"依赖地狱"。</li>
          </ul>
          <blockquote>工具是手段不是目的。能回答问题的是你的思路，软件只是把思路变成结果。先想清楚要算什么，再去选工具。</blockquote>


## 迷你实战

用 Conda 装一个工具并跑 `--help` 确认可用：

```bash
conda create -n t1 -c bioconda fastqc
conda activate t1
fastqc --help
```

观察：能打印帮助就装好了。Windows 用户优先用 WSL；装不动先 `conda clean -a` 再试。
