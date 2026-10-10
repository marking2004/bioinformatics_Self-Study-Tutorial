---
title: "常用生物信息数据库简介"
date: "2026-10-05"
weight: 30
category: "数据库"
meta: "资源 · 约 15 分钟"
draft: "false"
summary: "数据库是生信的'原料库'。本模块按数据类型给你一张地图，并讲清查询、下载、上传和在线分析四件基本操作。"
---

<p>数据库是生信的"原料库"。本模块按数据类型给你一张地图，并讲清查询、下载、上传和在线分析四件基本操作。</p>
          <h2>1. 主流数据库地图</h2>
          <table>
            <thead><tr><th>类型</th><th>代表库</th><th>存什么</th></tr></thead>
            <tbody>
              <tr><td>序列</td><td>NCBI、ENA、DDBJ</td><td>核酸 / 蛋白原始记录</td></tr>
              <tr><td>蛋白</td><td>UniProt、Pfam、InterPro</td><td>功能 / 结构域注释</td></tr>
              <tr><td>结构</td><td>PDB、AlphaFold DB</td><td>三维结构</td></tr>
              <tr><td>组学</td><td>GEO、SRA、ArrayExpress</td><td>表达 / 测序原始数据</td></tr>
              <tr><td>通路</td><td>KEGG、Reactome</td><td>代谢与信号通路</td></tr>
              <tr><td>分类</td><td>NCBI Taxonomy、ICTV</td><td>物种 / 病毒分类</td></tr>
              <tr><td>文献</td><td>PubMed</td><td>论文索引</td></tr>
            </tbody>
          </table>
          <h2>2. 查询</h2>
          <ul>
            <li>网页搜索：直接用基因名 / 登录号（如 NM_00001、P12345）；</li>
            <li><strong>Entrez / E-utilities</strong>：NCBI 的程序化查询接口（适合批量）；</li>
            <li>跨库检索：UniProt 可一键跳到对应 PDB / KEGG / GO。</li>
          </ul>
          <h2>3. 下载</h2>
          <ul>
            <li>单条：网页 "Send to / Download"；</li>
            <li>批量：<strong>FTP / Aspera</strong>（大文件），或 <code>esearch</code> + <code>efetch</code> 脚本；</li>
          </ul>
          <pre><code># 用 NCBI E-utilities 拉一批核酸
esearch -db nucleotide -query "Arabidopsis[orgn]" | \
  efetch -format fasta &gt; ara.fa</code></pre>
          <h2>4. 上传与在线分析</h2>
          <ul>
            <li><strong>上传</strong>：测序原始数据存 SRA（需申请登录号）；新序列可提交 GenBank；</li>
            <li><strong>在线分析</strong>：很多库自带工具——NCBI BLAST、EMBL-EBI 的 MSA / 结构预测、UniProt 的 BLAST 与功能预测，免安装即用。</li>
          </ul>
          <blockquote>引用数据时务必记录<strong>登录号（accession）</strong>和版本。数据库会更新，论文里写清版本，别人才能复现你的结果。</blockquote>


## 迷你实战

用 E-utilities 批量取一个基因家族的蛋白序列：

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=TP53[gene]&retmode=json"
# 取返回的 id 列表，再用 efetch 转成 FASTA
```

观察：把 `term` 换成任意"基因[gene]"或"基因[gene]+物种"组合即可批量取数；GEO/SRA 同理用 `esearch` + `efetch`。
