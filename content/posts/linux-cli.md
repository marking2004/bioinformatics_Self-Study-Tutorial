---
title: "Linux 与命令行：生信的第一课"
date: "2026-10-05"
weight: 10
category: "基础环境"
meta: "基础 · 约 15 分钟"
draft: "false"
summary: "生物信息学分析大多跑在 Linux 服务器上。不会命令行，寸步难行。
            这一课带你认识终端、文件系统，和几个每天都会用到的命令。先别怕——它只是另一种'说话方式'。"
---

<p>
            生物信息学分析大多跑在 Linux 服务器上。不会命令行，寸步难行。
            这一课带你认识终端、文件系统，和几个每天都会用到的命令。先别怕——它只是另一种"说话方式"。
          </p>
          <h2>1. 连上服务器 / 打开终端</h2>
          <p>本地是 Linux / Mac 直接打开 Terminal；Windows 推荐用 WSL（或 PuTTY）通过 ssh 登录服务器。</p>
          <pre><code>ssh student@bio.server.edu.cn
# 输入密码后即可在远程服务器上工作</code></pre>
          <h2>2. 看清你在哪：路径与目录</h2>
          <pre><code>pwd            # 显示当前所在目录
ls -l          # 长格式列出文件（含大小、时间、权限）
cd projects    # 进入 projects 目录
cd ..          # 返回上一级目录
mkdir raw      # 新建一个名为 raw 的目录</code></pre>
          <p><code>~</code> 代表你的家目录，<code>/</code> 代表根目录。生信里 <code>cd</code> 和 <code>ls</code> 的使用频率，大概和你呼吸一样高。</p>
          <h2>3. 看文件内容（别再用记事本打开 10G 的 fastq）</h2>
          <pre><code>head -n 5 seq.fq     # 看前 5 行
tail seq.fq         # 看末尾几行
wc -l seq.fq        # 统计行数
less seq.fq         # 分页浏览（按 q 退出）</code></pre>
          <p>大文件永远用 <code>head</code> / <code>less</code> 看，千万别双击用编辑器打开——它可能直接卡死。</p>
          <h2>4. 管道：把命令串起来</h2>
          <p>生信的精髓之一，是用 <code>|</code> 把一个命令的输出，直接喂给下一个命令。</p>
          <pre><code># 统计某个基因在结果里出现多少次
grep "GeneA" result.txt | wc -l

# 取第一列 → 排序 → 去重计数 → 看出现最多的前 20 个
cut -f 1 data.tsv | sort | uniq -c | head -20</code></pre>
          <h2>5. 一个稳妥的起步清单</h2>
          <table>
            <thead><tr><th>命令</th><th>作用</th><th>示例</th></tr></thead>
            <tbody>
              <tr><td><code>pwd</code></td><td>显示当前路径</td><td><code>pwd</code></td></tr>
              <tr><td><code>ls</code></td><td>列出文件</td><td><code>ls -lh</code></td></tr>
              <tr><td><code>cd</code></td><td>切换目录</td><td><code>cd raw</code></td></tr>
              <tr><td><code>grep</code></td><td>按模式搜索</td><td><code>grep "ATG" seq.fa</code></td></tr>
              <tr><td><code>|</code></td><td>管道串联</td><td><code>cmd1 | cmd2</code></td></tr>
            </tbody>
          </table>
          <h2>小结</h2>
          <p>命令行不可怕。先把这五个命令练熟，后面 90% 的生信流程都建立在这之上。下一模块我们会用这些命令去跑序列比对——到那时你会感谢今天耐心敲下的每一行。</p>


## 迷你实战

装好 Conda 后，用 `seqkit` 快速看任意 FASTA 的基本信息：

```bash
conda create -n bioinfo -c bioconda seqkit
conda activate bioinfo
curl -s "https://rest.uniprot.org/uniprotkb/P04637.fasta" -o demo.fasta
seqkit stat demo.fasta        # 序列条数、总长、最短/最长
seqkit fx2tab -l demo.fasta   # 每条序列长度
```

观察：`P04637` 长度约 393 aa。把 `P04637` 换成任意 accession 即可复用这套命令。
