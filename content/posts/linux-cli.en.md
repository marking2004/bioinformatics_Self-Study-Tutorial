---
title: "Linux & the Command Line: Your First Lesson"
date: "2026-10-05"
weight: 10
category: "Environment"
meta: "Basics · ~15 min"
draft: "false"
---

<p>
            Most bioinformatics runs on Linux servers. Without the command line you cannot move.
            This lesson introduces the terminal, the file system, and a few commands you will use every day. Don't panic — it is just another way of talking.
          </p>
          <h2>1. Connect to a server / open a terminal</h2>
          <p>On Linux / macOS just open Terminal; on Windows use WSL (or PuTTY) and log in via ssh.</p>
          <pre><code>ssh student@bio.server.edu.cn
# after the password you work on the remote server</code></pre>
          <h2>2. Know where you are: paths and directories</h2>
          <pre><code>pwd            # print working directory
ls -l          # long listing (size, time, permissions)
cd projects    # enter the projects directory
cd ..          # go up one level
mkdir raw      # create a directory named raw</code></pre>
          <p><code>~</code> is your home directory, <code>/</code> is the root. In bioinformatics, <code>cd</code> and <code>ls</code> are used about as often as you breathe.</p>
          <h2>3. Look at file contents (don't open a 10 GB fastq in Notepad)</h2>
          <pre><code>head -n 5 seq.fq     # first 5 lines
tail seq.fq         # last lines
wc -l seq.fq        # count lines
less seq.fq         # page through (press q to quit)</code></pre>
          <p>Always inspect big files with <code>head</code> / <code>less</code>. Never double-click them in an editor — it may freeze.</p>
          <h2>4. Pipes: chain commands together</h2>
          <p>One essence of bioinformatics is feeding a command's output straight into the next with <code>|</code>.</p>
          <pre><code># count how many times a gene appears
grep "GeneA" result.txt | wc -l

# column 1 -> sort -> unique count -> top 20
cut -f 1 data.tsv | sort | uniq -c | head -20</code></pre>
          <h2>5. A safe starter checklist</h2>
          <table>
            <thead><tr><th>Command</th><th>Purpose</th><th>Example</th></tr></thead>
            <tbody>
              <tr><td><code>pwd</code></td><td>print path</td><td><code>pwd</code></td></tr>
              <tr><td><code>ls</code></td><td>list files</td><td><code>ls -lh</code></td></tr>
              <tr><td><code>cd</code></td><td>change dir</td><td><code>cd raw</code></td></tr>
              <tr><td><code>grep</code></td><td>search by pattern</td><td><code>grep "ATG" seq.fa</code></td></tr>
              <tr><td><code>|</code></td><td>pipe</td><td><code>cmd1 | cmd2</code></td></tr>
            </tbody>
          </table>
          <h2>Summary</h2>
          <p>The command line is not scary. Master these five commands and 90% of later pipelines stand on them. Next module we run alignments with them — you will thank the lines you typed today.</p>


## Mini-case

After installing Conda, use `seqkit` to inspect any FASTA:

```bash
conda create -n bioinfo -c bioconda seqkit
conda activate bioinfo
curl -s "https://rest.uniprot.org/uniprotkb/P04637.fasta" -o demo.fasta
seqkit stat demo.fasta
seqkit fx2tab -l demo.fasta
```

Observe: `P04637` is ~393 aa. Swap `P04637` for any accession to reuse.
