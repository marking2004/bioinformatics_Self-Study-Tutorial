---
title: "实验 6：序列比对与 BLAST 搜索"
date: "2026-10-10"
weight: 60
category: "序列分析"
meta: "序列 · 约 50 分钟"
module: "sequence-alignment"
draft: false
summary: "BLAST 是生信用得最多的工具，也是被误读最多的。本实验讲清选哪个程序、搜哪个库，以及 E 值、一致度、覆盖率该怎么一起看。"
---

> 所属模块：[序列比对与 BLAST](../posts/sequence-alignment.html)

## 一、实验目的

<ul>
  <li>区分<strong>全局比对</strong>与<strong>局部比对</strong>，说清各自适用场合；</li>
  <li>根据"我手上是什么、想找什么"选对 BLAST 程序与数据库；</li>
  <li>会用网页 BLAST 与命令行 BLAST+，能批量跑并解析表格结果；</li>
  <li>正确解读 E 值、一致度与覆盖率，避免"相似度 70% 就是同一个基因"这类误判。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>NCBI BLAST（网页）</td><td>快速查库</td><td><a href="https://blast.ncbi.nlm.nih.gov/Blast.cgi" target="_blank" rel="noopener">NCBI BLAST</a></td></tr>
    <tr><td>BLAST+ 命令行</td><td>批量、本地建库</td><td><a href="https://blast.ncbi.nlm.nih.gov/doc/blast-topics/" target="_blank" rel="noopener">官方文档</a></td></tr>
    <tr><td>EMBOSS needle / water</td><td>双序列全局 / 局部比对</td><td><a href="https://www.ebi.ac.uk/Tools/psa/" target="_blank" rel="noopener">网页版</a></td></tr>
    <tr><td>UniProt / RefSeq</td><td>常用蛋白与参考序列库</td><td><a href="https://www.uniprot.org/" target="_blank" rel="noopener">UniProt</a></td></tr>
  </tbody>
</table>

## 三、操作步骤

**1. 先选程序：我手上是什么，想找什么**

<table>
  <thead><tr><th>查询序列</th><th>搜索库</th><th>用哪个程序</th></tr></thead>
  <tbody>
    <tr><td>核酸</td><td>核酸</td><td><code>blastn</code></td></tr>
    <tr><td>核酸（想翻译成蛋白再比）</td><td>蛋白</td><td><code>blastx</code></td></tr>
    <tr><td>蛋白</td><td>蛋白</td><td><code>blastp</code></td></tr>
    <tr><td>蛋白</td><td>核酸（库被翻译后比对）</td><td><code>tblastn</code></td></tr>
  </tbody>
</table>

> 关键原则：<strong>远缘同源搜索用蛋白比核酸更灵敏</strong>。因为遗传密码冗余，核酸序列变了氨基酸可能没变。查 distant homolog 时优先 blastp / tblastn。

**2. 网页 BLAST**

打开 NCBI BLAST，粘贴序列 → 选程序 → 选数据库（<code>nr/nt</code> 全库，或 <code>RefSeq</code> 更整齐）→ 在 <em>Organism</em> 里限定物种可大幅减少噪声 → <em>BLAST</em>。

结果页看三块：<em>Graphic Summary</em>（命中分布与得分）、<em>Descriptions</em>（一览表）、<em>Alignments</em>（逐条比对细节）。

**3. 结果里每个数字是什么意思**

<table>
  <thead><tr><th>指标</th><th>含义</th><th>怎么用</th></tr></thead>
  <tbody>
    <tr><td>Score / Bitscore</td><td>比对得分，越高越好</td><td>横向比较同一查询的不同命中</td></tr>
    <tr><td>E-value</td><td>在这么大的库里随机出现同等得分的期望次数</td><td>越小越可信；<code>1e-5</code> 是常用门槛，但不是绝对标准</td></tr>
    <tr><td>Percent identity</td><td>一致残基比例</td><td>看"有多像"</td></tr>
    <tr><td>Query cover</td><td>查询序列被覆盖的比例</td><td>看"比了多长"，全长还是只有一小段结构域</td></tr>
  </tbody>
</table>

**4. 命令行 BLAST+**

```bash
# 建库
makeblastdb -in refs.fasta -dbtype nucl -out mydb

# 搜索，输出制表格式
blastn -query q.fasta -db mydb \
  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" \
  -evalue 1e-5 -max_target_seqs 10 -num_threads 4 > hits.tsv

blastp -query prot.fasta -db uniprot -evalue 1e-3 -outfmt 6 > hits.tsv
```

`outfmt 6` 的表格可直接用 R / Python / Excel 打开排序筛选，适合几十上百条查询批量跑。

**5. 双序列比对：全局 vs 局部**

```bash
needle -asequence a.fasta -bsequence b.fasta -gapopen 10 -gapextend 0.5 -outfile out.needle  # 全局
water  -asequence a.fasta -bsequence b.fasta -gapopen 10 -gapextend 0.5 -outfile out.water   # 局部
```

<ul>
  <li><strong>全局（Needleman-Wunsch）</strong>：两条序列从头比到尾，适合长度相近、整体同源的两条序列。</li>
  <li><strong>局部（Smith-Waterman，BLAST 的原型）</strong>：只找最优片段，适合一条长序列里找保守结构域。</li>
</ul>

## 四、结果判读

<ul>
  <li><strong>E 值不是"相似度"</strong>：它衡量"这个得分有多可能是随机产生的"。库越大，同样得分的 E 值越大。跨库比较 E 值没有意义。</li>
  <li><strong>必须同时看一致度与覆盖率</strong>：identity 95% 但 query cover 只有 8%，说明只是某个短结构域相似，不能推断整条序列同源。</li>
  <li><strong>相似不等于同源，同源不等于功能相同</strong>：高分命中只能说明序列相似；功能注释要回到 UniProt 看实验证据，同家族不同成员功能可能已分化。</li>
  <li><strong>最佳命中不等于正确注释</strong>：库里若有错误注释的序列，你也会"继承"这个错误。看命中的物种分布与一致性，别只抄第一名。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>程序选错</strong>：拿核酸序列去搜亲缘很远的物种，blastn 常常什么也搜不到，换成 blastx 就有结果。</li>
  <li><strong>低复杂度区域</strong>：BLAST 默认屏蔽这类区域（如 poly-A、简单重复），若你特意要找它们，需手动关闭过滤。</li>
  <li><strong>nr 库巨大且冗余</strong>：同一蛋白有几十条几乎相同的记录，结果表看起来很长其实信息量小。改用 UniProt/RefSeq 或聚类版本更清爽。</li>
  <li><strong>阈值照搬他人</strong>：<code>1e-5</code> 只是习惯值。短序列、小库、远缘搜索都要重新考虑。</li>
</ul>

## 六、练习

<ol>
  <li>取一条你研究物种的核酸序列，网页 BLAST 后记录最佳命中的 accession、identity、query cover 与 E 值。</li>
  <li>换用 blastx 再搜一次，比较命中数量与最佳 E 值的变化，说明原因。</li>
  <li>命令行对本地 5 条序列建库并搜索，导出 <code>outfmt 6</code> 表格，用 Excel 按 bitscore 排序。</li>
  <li>用 <code>water</code> 比对两条序列，报告局部最优片段的长度与一致度。</li>
  <li>（选做）限定物种后重搜，比较不限定与限定的结果差异。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://blast.ncbi.nlm.nih.gov/doc/blast-topics/" target="_blank" rel="noopener">BLAST 官方使用说明</a></li>
  <li><a href="https://www.ncbi.nlm.nih.gov/books/NBK1734/" target="_blank" rel="noopener">BLAST 上手教程（NCBI Bookshelf）</a></li>
  <li><a href="https://www.ebi.ac.uk/Tools/psa/" target="_blank" rel="noopener">EMBOSS 双序列比对工具</a></li>
</ul>
