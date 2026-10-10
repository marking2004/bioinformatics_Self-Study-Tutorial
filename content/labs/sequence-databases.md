---
title: "实验 4：分子序列数据库与记录格式"
date: "2026-10-10"
weight: 40
category: "数据库"
meta: "资源 · 约 40 分钟"
module: "databases"
draft: false
summary: "同一条序列在不同数据库里有不同的'包装'。本实验带你逐字段读懂 GenBank 记录，分辨一级库与二级库，并掌握限定字段的检索写法。"
---

> 所属模块：[常用生物信息数据库简介](../posts/databases.html)

## 一、实验目的

<ul>
  <li>分清<strong>一级库</strong>（原始提交）与<strong>二级库</strong>（人工/计算再注释）的分工；</li>
  <li>逐字段读懂一条 GenBank 记录，知道每个字段能回答什么问题；</li>
  <li>掌握带限定字段的检索语法，避免"搜出来三千条有用的在最后一页"；</li>
  <li>能把检索到的记录导出成 FASTA 并做格式转换。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>数据库 / 工具</th><th>类型</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>NCBI GenBank</td><td>一级核酸库</td><td><a href="https://www.ncbi.nlm.nih.gov/genbank/" target="_blank" rel="noopener">NCBI</a></td></tr>
    <tr><td>ENA（EBI）</td><td>一级核酸库</td><td><a href="https://www.ebi.ac.uk/ena" target="_blank" rel="noopener">ENA</a></td></tr>
    <tr><td>DDBJ</td><td>一级核酸库</td><td><a href="https://www.ddbj.nig.ac.jp/" target="_blank" rel="noopener">DDBJ</a></td></tr>
    <tr><td>UniProt</td><td>二级蛋白库</td><td><a href="https://www.uniprot.org/" target="_blank" rel="noopener">UniProt</a></td></tr>
    <tr><td>PDB / InterPro</td><td>结构 / 功能域</td><td><a href="https://www.rcsb.org/" target="_blank" rel="noopener">RCSB PDB</a> · <a href="https://www.ebi.ac.uk/interpro/" target="_blank" rel="noopener">InterPro</a></td></tr>
    <tr><td>NGDC</td><td>国家级数据中心</td><td><a href="https://ngdc.cncb.ac.cn/" target="_blank" rel="noopener">国家基因组科学数据中心</a></td></tr>
  </tbody>
</table>

<p>三家一级库（GenBank / ENA / DDBJ）组成 <strong>INSDC</strong>，数据每日同步，同一条记录在三家的 accession 相同——所以取不到时可以换一家试试。</p>

## 三、操作步骤

**1. 打开一条记录，逐字段读**

以 GenBank 记录为例（可用任意一个 accession，如 <code>EF069996</code>），记录从上到下分成几块：

<table>
  <thead><tr><th>字段</th><th>回答什么问题</th></tr></thead>
  <tbody>
    <tr><td>LOCUS</td><td>记录名、长度、分子类型、提交日期</td></tr>
    <tr><td>DEFINITION</td><td>一句话描述这条序列是什么</td></tr>
    <tr><td>ACCESSION / VERSION</td><td>唯一编号；VERSION 是"编号.版本"，序列改动版本递增</td></tr>
    <tr><td>KEYWORDS / SOURCE</td><td>关键词、物种与分类位置</td></tr>
    <tr><td>REFERENCE</td><td>相关文献，注释可信度的重要线索</td></tr>
    <tr><td>FEATURES</td><td>注释主体：CDS、mRNA、exon、结构域位置等</td></tr>
    <tr><td>ORIGIN</td><td>真正的序列，每行 60 个碱基并标了行号</td></tr>
  </tbody>
</table>

**2. FASTA 与 GenBank 的区别**

```
>EF069996.1 Oryza sativa ...        ← FASTA：只保留 ID + 描述 + 序列
ATGCGTACGG...
```

FASTA 轻、快、工具通吃，但<strong>丢掉了全部结构注释</strong>。做基因结构、CDS、外显子分析时必须用 GenBank（或 EMBL）格式。

**3. 用限定字段检索**

在 NCBI 搜索框里直接写：<code>Oryza sativa[Organism] AND NHX[Gene Name]</code>。常用限定符：

<ul>
  <li><code>[Organism]</code> 物种；<code>[Gene Name]</code> 基因名；<code>[Accession]</code> 编号；</li>
  <li><code>[Publication Date]</code> 时间范围；<code>[Sequence Length]</code> 长度范围；</li>
  <li><code>AND</code> / <code>OR</code> / <code>NOT</code> 组合条件。</li>
</ul>

**4. 导出与格式转换**

NCBI 记录页 → <em>Send to</em> → <em>Complete Record</em> → <em>File</em> → 选 FASTA 或 GenBank 保存。命令行转换可用：

```bash
seqkit seq -w 0 in.fasta > out_oneline.fasta    # 序列换行改为单行
seqkit fx2tab in.fasta | head                    # 转成表格查看
```

**5. 看一条蛋白记录**

打开 UniProt 对应条目，重点看 <em>Function</em>、<em>Family &amp; Domains</em>、<em>Sequence</em> 三栏。UniProt 的注释带<strong>证据等级</strong>：实验证据 &gt; 计算预测，写报告引用时要区分。

**6. 了解国产数据源**

浏览 <a href="https://ngdc.cncb.ac.cn/" target="_blank" rel="noopener">NGDC</a>，看其基因组、转录组与变异数据的入口。国内项目的数据常先在这里发布。

## 四、结果判读

<ul>
  <li><strong>ACCESSION 与 VERSION 不是一回事</strong>：论文里应引用带版本的编号（如 <code>EF069996.1</code>），否则别人无法确认你用的是哪一版序列。</li>
  <li><strong>RefSeq 前缀有含义</strong>：<code>NC_</code> 基因组、<code>NM_</code> mRNA、<code>NP_</code> 蛋白、<code>NR_</code> 非编码 RNA；带下划线前缀的是 NCBI 重新注释的参考序列，比原始提交更整齐，但更新有滞后。</li>
  <li><strong>FEATURES 里的 CDS 位置</strong>：出现 <code>join(...)</code> 说明有内含子；<code>complement(...)</code> 说明基因在负链。</li>
  <li>记录页 <em>Comment</em> 里常注明序列是否完整（partial）、是否由预测得来——这直接影响后续结论。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>同一基因多条记录</strong>：不同品种、不同提交者会有多条高度相似的序列，做比对前先确定用哪条做参考。</li>
  <li><strong>物种名变更</strong>：分类学改名后，旧记录里的物种名可能过时，检索时用新名搜不到旧记录。</li>
  <li><strong>预测序列与实测序列混用</strong>：注释里写 <em>by similarity</em> 或 <em>predicted</em> 的是预测结果，不能直接当实验证据。</li>
  <li><strong>只看 FASTA 就下结论</strong>：FASTA 里看不到结构注释，容易把一条 mRNA 当成基因组序列。</li>
</ul>

## 六、练习

<ol>
  <li>检索拟南芥（<em>Arabidopsis thaliana</em>）NHX 基因的核酸记录，记下 accession 与序列长度。</li>
  <li>分别下载该记录的 FASTA 与 GenBank 两个版本，比较文件大小并说明差异来源。</li>
  <li>在 UniProt 找到对应蛋白，写出其长度、功能一句话描述与所属家族。</li>
  <li>用限定字段检索"水稻 + 2020 年以后提交 + 长度大于 1000 bp"的记录，写出检索式。</li>
  <li>（选做）在 NGDC 上找一个与你专业相关的物种基因组，记录其数据编号与入口页面。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://www.ncbi.nlm.nih.gov/genbank/samplerecord/" target="_blank" rel="noopener">GenBank 记录样例与字段说明</a></li>
  <li><a href="https://www.insdc.org/" target="_blank" rel="noopener">INSDC 官方说明</a></li>
  <li><a href="https://www.uniprot.org/help/text-search" target="_blank" rel="noopener">UniProt 检索语法</a></li>
  <li><a href="https://seqkit.usamimi.info/" target="_blank" rel="noopener">SeqKit 文档</a></li>
</ul>
