---
title: "Lab 1: The Linux Command Line and File Management"
date: "2026-10-10"
weight: 10
category: "Environment"
meta: "Basics · ~40 min"
module: "linux-cli"
draft: false
summary: "Bioinformatics almost always runs on Linux. This lab walks the terminal, the file system, pipes and redirection, drills the dozen commands you use every day, and installs your first tool."
---

> Module: [Linux & the Command Line](../posts/linux-cli.html)

## 1. Goals

<ul>
  <li>Understand the Linux directory tree and move around it with commands;</li>
  <li>Create, delete, rename and batch-handle files and directories;</li>
  <li>Grasp <strong>pipes and redirection</strong> — the real source of the shell's power;</li>
  <li>Edit text with <code>vim</code> and install software with <code>conda</code>.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool / environment</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>Linux terminal</td><td>command execution</td><td><a href="https://learn.microsoft.com/windows/wsl/install" target="_blank" rel="noopener">WSL (Windows users)</a></td></tr>
    <tr><td>GNU coreutils</td><td>ls / cp / mv and friends</td><td><a href="https://www.gnu.org/software/coreutils/" target="_blank" rel="noopener">gnu.org</a></td></tr>
    <tr><td>vim</td><td>text editing in the terminal</td><td><a href="https://www.vim.org/" target="_blank" rel="noopener">vim.org</a></td></tr>
    <tr><td>conda / mamba</td><td>software and dependency management</td><td><a href="https://docs.conda.io/projects/miniconda/en/latest/" target="_blank" rel="noopener">Miniconda</a> · <a href="https://bioconda.github.io/" target="_blank" rel="noopener">Bioconda</a></td></tr>
  </tbody>
</table>

<p>On Windows, install WSL2 (Ubuntu) for a genuine Linux environment. A lab server works equally well — the commands are identical.</p>

## 3. Procedure

**1. Where am I, what is here**

```bash
pwd                 # print working directory
ls                  # list contents
ls -lh              # long format, human-readable sizes
ls -a               # include hidden files (leading dot)
```

**2. Moving and creating**

```bash
cd ~                # go home
mkdir bioinfo_lab   # make a directory
cd bioinfo_lab      # enter it
touch README.txt    # create an empty file
```

**3. Copy, move, rename, delete**

```bash
cp README.txt README.bak     # copy
mv README.bak notes.txt      # move / rename
rm notes.txt                 # delete a file
rm -r bioinfo_lab            # delete a directory (recursive)
```

> `rm` does not go to a trash bin. Run `ls` first to confirm the target, especially with `-r` or `-f`.

**4. Looking inside files**

```bash
cat seq.fasta        # dump everything (small files)
less seq.fasta       # paged view, press q to quit (large files)
head -20 seq.fasta   # first 20 lines
tail -5  seq.fasta   # last 5 lines
wc -l seq.fasta      # count lines
```

**5. Searching, pipes and redirection**

```bash
grep ">" seq.fasta            # every header line
grep -c ">" seq.fasta         # count the sequences
ls -lh | grep "fasta"         # pipe: feed one command's output to the next
grep ">" seq.fasta > ids.txt  # redirect: write to file (overwrite)
grep ">" seq.fasta >> ids.txt # append
```

> Pipes `|` plus redirection `>` are what replace manual clicking. They are how you process hundreds of files at once.

**6. Permissions and archives**

```bash
chmod +x run.sh      # make a script executable
tar -czf data.tar.gz data/    # pack and compress
tar -xzf data.tar.gz          # unpack
gzip -d file.fq.gz            # decompress gz (the usual sequencing format)
```

**7. Editing with vim**

```bash
vim hello.txt
```

vim has three states you will use: opening a file puts you in <strong>normal mode</strong>; press `i` for <strong>insert mode</strong>; press `Esc` to return to normal mode, then `:w` to save, `:q` to quit, `:wq` to save and quit, `:q!` to quit without saving.

**8. Install your first tool**

```bash
conda install -c bioconda seqkit -y
seqkit stats seq.fasta
```

## 4. Reading the results

<ul>
  <li>In <code>ls -lh</code> output the first column looks like <code>-rw-r--r--</code>: the leading <code>-</code> means a regular file, <code>d</code> a directory; the three <code>rw-</code> groups are permissions for owner, group and others.</li>
  <li><code>seqkit stats</code> reports number of sequences, total length and shortest/longest. Run it on any new FASTA to spot empty or truncated files immediately.</li>
  <li>In FASTA, lines starting with <code>&gt;</code> are headers, so <code>grep -c "&gt;"</code> should match the expected sequence count.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Case matters</strong>: <code>Data</code> and <code>data</code> are different directories.</li>
  <li><strong>Spaces in filenames</strong>: the shell reads them as two arguments. Quote them (<code>"my file.txt"</code>) or use underscores.</li>
  <li><strong>Windows line endings</strong>: scripts edited on Windows often fail with <code>^M: bad interpreter</code>. Convert with <code>dos2unix</code>.</li>
  <li><strong>Disk full</strong>: sequencing data runs to tens of GB. Check <code>df -h</code> before a long pipeline.</li>
</ul>

## 6. Exercises

<ol>
  <li>Create <code>lab01</code> in your home directory with subdirectories <code>data</code> and <code>result</code>.</li>
  <li>Write a FASTA file with three sequences and count the sequences with a single command.</li>
  <li>Save the output of <code>ls -lh</code> to <code>result/list.txt</code>.</li>
  <li>Use <code>vim</code> to write <code>run.sh</code> containing <code>echo "hello lab01"</code>, make it executable and run it.</li>
  <li>(Optional) Run <code>seqkit</code> on a real downloaded FASTA and record the sequence count and total length.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://www.gnu.org/software/coreutils/manual/" target="_blank" rel="noopener">GNU Coreutils manual</a></li>
  <li><a href="https://swcarpentry.github.io/shell-novice/" target="_blank" rel="noopener">Software Carpentry: The Unix Shell</a></li>
  <li><a href="https://seqkit.usamimi.info/" target="_blank" rel="noopener">SeqKit documentation</a></li>
</ul>
