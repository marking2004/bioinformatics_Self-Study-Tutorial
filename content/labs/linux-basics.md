---
title: "实验 1：Linux 命令行与文件管理"
date: "2026-10-10"
weight: 10
category: "环境配置"
meta: "基础 · 约 40 分钟"
module: "linux-cli"
draft: false
summary: "生信分析几乎都跑在 Linux 上。本实验从终端、文件系统到管道与重定向，练会每天都要用的十几个命令，并装上第一个工具。"
---

> 所属模块：[Linux 与命令行](../posts/linux-cli.html)

## 一、实验目的

<ul>
  <li>理解 Linux 的目录树结构，能用命令在文件系统里自由移动；</li>
  <li>掌握文件与目录的增、删、改、查与批量操作；</li>
  <li>理解<strong>管道与重定向</strong>——这是命令行真正强大的地方；</li>
  <li>能用 <code>vim</code> 编辑文本文件，能用 <code>conda</code> 安装软件。</li>
</ul>

## 二、你将用到

<table>
  <thead><tr><th>工具 / 环境</th><th>用途</th><th>官方链接</th></tr></thead>
  <tbody>
    <tr><td>Linux 终端</td><td>命令执行环境</td><td><a href="https://learn.microsoft.com/windows/wsl/install" target="_blank" rel="noopener">WSL（Windows 用户）</a></td></tr>
    <tr><td>GNU coreutils</td><td>ls / cp / mv 等基础命令</td><td><a href="https://www.gnu.org/software/coreutils/" target="_blank" rel="noopener">gnu.org</a></td></tr>
    <tr><td>vim</td><td>终端内文本编辑</td><td><a href="https://www.vim.org/" target="_blank" rel="noopener">vim.org</a></td></tr>
    <tr><td>conda / mamba</td><td>软件与依赖管理</td><td><a href="https://docs.conda.io/projects/miniconda/en/latest/" target="_blank" rel="noopener">Miniconda</a> · <a href="https://bioconda.github.io/" target="_blank" rel="noopener">Bioconda</a></td></tr>
  </tbody>
</table>

<p>Windows 用户推荐装 WSL2（Ubuntu），可得到一个真正的 Linux 环境；不想装系统的话，用服务器或机房的 Linux 机器也可，命令完全一致。</p>

## 三、操作步骤

**1. 定位自己在哪、周围有什么**

```bash
pwd                 # 显示当前目录（print working directory）
ls                  # 列出当前目录内容
ls -lh              # 详细列表，文件大小以人类可读形式显示
ls -a               # 含隐藏文件（以 . 开头）
```

**2. 移动与创建**

```bash
cd ~                # 回到家目录
mkdir bioinfo_lab   # 新建目录
cd bioinfo_lab      # 进入目录
touch README.txt    # 新建空文件
```

**3. 复制、移动、重命名、删除**

```bash
cp README.txt README.bak     # 复制
mv README.bak notes.txt      # 移动 / 重命名
rm notes.txt                 # 删除文件
rm -r bioinfo_lab            # 删除目录（-r 递归）
```

> `rm` 删除后不进回收站。执行前先 `ls` 确认对象，尤其是带 `-r`、`-f` 的时候。

**4. 查看文件内容**

```bash
cat seq.fasta        # 全文输出（适合小文件）
less seq.fasta       # 分页查看，q 退出（大文件用这个）
head -20 seq.fasta   # 看前 20 行
tail -5  seq.fasta   # 看后 5 行
wc -l seq.fasta      # 统计行数
```

**5. 搜索、管道与重定向**

```bash
grep ">" seq.fasta            # 找出所有序列标题行
grep -c ">" seq.fasta         # 统计序列条数
ls -lh | grep "fasta"         # 管道：把前一个命令的输出交给后一个
grep ">" seq.fasta > ids.txt  # 重定向：结果写入文件（覆盖）
grep ">" seq.fasta >> ids.txt # 追加写入
```

> 管道 `|` 与重定向 `>` 的组合，是命令行替代"手工点选"的关键。一次处理几百个文件靠的就是它。

**6. 权限与压缩**

```bash
chmod +x run.sh      # 给脚本加可执行权限
tar -czf data.tar.gz data/    # 打包压缩
tar -xzf data.tar.gz          # 解压
gzip -d file.fq.gz            # 解压 gz（测序数据常见格式）
```

**7. 用 vim 编辑文件**

```bash
vim hello.txt
```

vim 有三种常用状态：打开文件是<strong>普通模式</strong>；按 `i` 进入<strong>编辑模式</strong>；编辑完按 `Esc` 回到普通模式，输入 `:w` 保存、`:q` 退出、`:wq` 保存并退出、`:q!` 强制不保存退出。

**8. 安装第一个生信工具**

```bash
conda install -c bioconda seqkit -y
seqkit stats seq.fasta
```

## 四、结果判读

<ul>
  <li><code>ls -lh</code> 输出的第一列如 <code>-rw-r--r--</code>，首字符 <code>-</code> 是普通文件、<code>d</code> 是目录；后面三组 <code>rw-</code> 分别是所有者、同组、其他人的权限。</li>
  <li><code>seqkit stats</code> 会给出序列条数、总长度、最短/最长序列——拿到一个 FASTA 文件先跑它，能立刻发现文件是否为空、是否被截断。</li>
  <li>FASTA 文件里以 <code>&gt;</code> 开头的行是序列标题，<code>grep -c "&gt;"</code> 得到的条数应与预期一致。</li>
</ul>

## 五、常见坑

<ul>
  <li><strong>路径大小写</strong>：Linux 区分大小写，<code>Data</code> 与 <code>data</code> 是两个目录。</li>
  <li><strong>文件名带空格</strong>：会被当成两个参数。要么用引号 <code>"my file.txt"</code>，要么避免空格，用下划线。</li>
  <li><strong>Windows 换行符</strong>：在 Windows 下编辑的脚本拿到 Linux 跑，常因 <code>\r\n</code> 报 <code>^M: bad interpreter</code>。用 <code>dos2unix</code> 转换。</li>
  <li><strong>磁盘写满</strong>：测序数据动辄几十 GB，跑流程前 <code>df -h</code> 看一眼剩余空间。</li>
</ul>

## 六、练习

<ol>
  <li>在家目录下建 <code>lab01</code>，在其中建 <code>data</code>、<code>result</code> 两个子目录。</li>
  <li>写一个含 3 条序列的 FASTA 文件，用一条命令统计其中序列条数。</li>
  <li>把 <code>ls -lh</code> 的结果保存到 <code>result/list.txt</code>。</li>
  <li>用 <code>vim</code> 写一个 <code>run.sh</code>，内容为 <code>echo "hello lab01"</code>，加权限并执行。</li>
  <li>（选做）用 <code>seqkit</code> 统计一个真实下载的 FASTA 文件，记录序列数与总长度。</li>
</ol>

## 延伸资源

<ul>
  <li><a href="https://www.gnu.org/software/coreutils/manual/" target="_blank" rel="noopener">GNU Coreutils 手册</a></li>
  <li><a href="https://swcarpentry.github.io/shell-novice/" target="_blank" rel="noopener">Software Carpentry: The Unix Shell</a></li>
  <li><a href="https://seqkit.usamimi.info/" target="_blank" rel="noopener">SeqKit 文档</a></li>
</ul>
