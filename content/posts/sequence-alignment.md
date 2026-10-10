---
title: "序列比对与 BLAST：从一条序列找同源基因"
date: "2026-10-05"
weight: 40
category: "序列分析"
meta: "序列 · 约 12 分钟"
draft: "false"
summary: "比对（alignment）是生物信息学的'语法'。当你拿到一条未知序列，第一件事往往是问：它和已知的谁比较像？这，就是 BLAST 在做的事。"
---

<p>比对（alignment）是生物信息学的"语法"。当你拿到一条未知序列，第一件事往往是问：它和已知的谁比较像？这，就是 BLAST 在做的事。</p>
          <h2>1. 为什么要比对</h2>
          <p>两条序列"像"，通常意味着它们有共同祖先或相似功能。比对就是把序列上下对齐，标出哪些位置一致、哪些发生了变异——这是几乎所有下游分析的解释基础。</p>
          <h2>2. BLAST 是怎么工作的（直觉版）</h2>
          <p>BLAST 不会暴力比对所有序列（那样太慢），而是先找短的"种子"高相似片段（seed），再向两端延伸。所以它快，且对绝大多数场景够准。</p>
          <ul>
            <li>输入你的查询序列（query）；</li>
            <li>在数据库中找短的、高度相似的种子片段；</li>
            <li>把种子向两端延伸成局部比对；</li>
            <li>用 E 值评估这次匹配是否显著（E 值越小越可信）。</li>
          </ul>
          <h2>3. 在命令行跑一次 BLAST（示例）</h2>
          <pre><code># 用本地 blastn 把 query.fa 比对到 nt 数据库
blastn -query query.fa -db nt -out result.tsv \
       -outfmt 6 -evalue 1e-5 -num_threads 4</code></pre>
          <p><code>-outfmt 6</code> 输出制表符分隔的简洁表格，方便后面用上节课学的 <code>cut</code> / <code>sort</code> 处理。</p>
          <h2>4. 读懂结果：E 值与比特分</h2>
          <table>
            <thead><tr><th>字段</th><th>含义</th></tr></thead>
            <tbody>
              <tr><td>E value</td><td>随机匹配到同样好的概率，越小越可靠</td></tr>
              <tr><td>Bitscore</td><td>比对得分，越大越相似</td></tr>
              <tr><td>% identity</td><td>一致性百分比</td></tr>
            </tbody>
          </table>
          <p>别被高一致性骗了：如果两条序列都很短，即使 100% 一致也可能不可信——一定要看 E 值。</p>
          <h2>5. 成对比对 vs 数据库比对</h2>
          <p>把单条序列拿去搜数据库（如 NCBI 的 blastn）叫<strong>数据库搜索</strong>；而把两条序列直接对齐（如 Needleman-Wunsch 全局比对、Smith-Waterman 局部比对）叫<strong>成对比对</strong>，用于精细比较两条序列。</p>
          <blockquote>比对的本质，是在"错配"和"空位"之间找平衡；空位罚分（gap penalty）决定了最终比对长什么样。</blockquote>


## 迷你实战

拿两段 DNA 序列做核酸 blastn（先建库）：

```bash
# 把参考序列放进 subject.fa，查询序列放进 query.fa
makeblastdb -in subject.fa -dbtype nucl
blastn -query query.fa -db subject.fa -outfmt 6
```

观察：表格最后一列 `evalue` 越小越显著；一致度看 `pident`。先用 NCBI 网页 BLAST 直观感受，再回到命令行批量跑。
