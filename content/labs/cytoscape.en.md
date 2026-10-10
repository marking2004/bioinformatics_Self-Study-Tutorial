---
title: "Lab 18: Network Construction and Analysis with Cytoscape"
date: "2026-10-10"
weight: 180
category: "Networks"
meta: "Networks · ~50 min"
module: "multi-omics"
draft: false
summary: "Genes, proteins and interactions from earlier labs end up as a network. This lab builds one in Cytoscape, runs topological analysis, finds modules and hubs, and covers figure export that survives peer review."
---

> Module: [Multi-omics Integration](../posts/multi-omics.html)

## 1. Goals

<ul>
  <li>Learn the vocabulary of networks: node, edge, degree, centrality and module;</li>
  <li>Build a network from STRING or a custom edge list and map expression onto it;</li>
  <li>Run NetworkAnalyzer, MCODE and cytoHubba;</li>
  <li>Export publication-grade figures and know the limits of network conclusions.</li>
</ul>

## 2. What you will use

<table>
  <thead><tr><th>Tool / database</th><th>Purpose</th><th>Official link</th></tr></thead>
  <tbody>
    <tr><td>Cytoscape</td><td>network analysis and visualisation platform</td><td><a href="https://cytoscape.org/" target="_blank" rel="noopener">cytoscape.org</a></td></tr>
    <tr><td>STRING</td><td>protein-protein interaction source</td><td><a href="https://string-db.org/" target="_blank" rel="noopener">STRING</a></td></tr>
    <tr><td>BioGRID / GeneMANIA</td><td>interactions and functional associations</td><td><a href="https://thebiogrid.org/" target="_blank" rel="noopener">BioGRID</a> · <a href="https://genemania.org/" target="_blank" rel="noopener">GeneMANIA</a></td></tr>
    <tr><td>MCODE / cytoHubba</td><td>modules and hub nodes</td><td>install from the Cytoscape App Store</td></tr>
    <tr><td>ClueGO / EnrichmentMap</td><td>enrichment on networks</td><td>install from the Cytoscape App Store</td></tr>
  </tbody>
</table>

## 3. Procedure

**1. Prepare the data**

Two routes:

<ul>
  <li><strong>Build from STRING</strong>: enter a gene list (for example your DE genes), set a confidence threshold, export TSV or import directly inside Cytoscape via <em>stringApp</em>;</li>
  <li><strong>Custom edge list</strong>: a two-column CSV (source / target), such as miRNA–target or lncRNA–miRNA pairs.</li>
</ul>

**2. Import**

<em>File → Import → Network from File</em> for the edge list; <em>File → Import → Table from File</em> for node attributes (log2FC, padj, module assignment).

**3. Map visual style**

In the <em>Style</em> panel:

<ul>
  <li><strong>node colour</strong> to log2FC (red up, blue down, or your own convention);</li>
  <li><strong>node size</strong> to degree or significance;</li>
  <li><strong>edge width / opacity</strong> to interaction confidence (e.g. STRING score).</li>
</ul>

**4. Layout**

Use <em>Layout → Prefuse Force Directed Layout</em>, which clusters connected nodes naturally. Lay out before analysing — otherwise no structure is visible.

**5. Topological analysis**

<em>Tools → NetworkAnalyzer → Network Analysis → Analyze Network</em> reports:

<ul>
  <li><strong>Degree</strong>: how many edges a node has — the most direct importance measure;</li>
  <li><strong>Betweenness</strong>: how many shortest paths pass through it; high values mark bridge nodes;</li>
  <li><strong>Clustering coefficient</strong>: how tightly a node's neighbours interconnect.</li>
</ul>

**6. Modules and hubs**

<ul>
  <li><strong>MCODE</strong>: <em>Apps → MCODE</em> finds densely connected sub-networks, useful for pulling functional modules out of a large network;</li>
  <li><strong>cytoHubba</strong>: ranks hubs by MCC, Degree, EPC and other algorithms; take the top 10–20 as candidates.</li>
</ul>

**7. Functional annotation**

<em>Apps → ClueGO</em> runs GO / KEGG enrichment per module, or use <em>EnrichmentMap</em> to draw the enrichment results themselves as a network (nodes are terms, edges are shared genes).

**8. Export**

<em>File → Export → Network to Image</em> and choose PDF or SVG (vector) at 300 dpi or more. Never submit a screenshot.

## 4. Reading the results

<ul>
  <li><strong>Degree distribution</strong>: biological networks are roughly scale-free — a few hubs, many poorly connected nodes. A uniform distribution usually means a data-source or threshold problem.</li>
  <li><strong>What the STRING threshold means</strong>: medium confidence is about 0.4, high confidence 0.7. Higher thresholds give fewer, more reliable edges but miss real interactions. Always state the threshold you used.</li>
  <li><strong>Hubs are candidates</strong>: a high degree says the node is well connected in existing data, which is partly a study-bias effect — well-studied genes accumulate more interaction records.</li>
  <li><strong>Networks show association, not causation</strong>: an edge means a reported interaction or co-expression, not a direction or magnitude of regulation.</li>
</ul>

## 5. Common pitfalls

<ul>
  <li><strong>Hairball figures</strong>: a thousand unlaid-out nodes carry no information. Filter by degree or significance and show the core sub-network.</li>
  <li><strong>ID mismatches</strong>: node IDs in the attribute table must match the network exactly (case, version suffix) or nothing maps.</li>
  <li><strong>Unstated thresholds</strong>: the same gene list at 0.4 and 0.7 gives different networks. Without the threshold the result is irreproducible.</li>
  <li><strong>Treating PPI as regulation</strong>: physical interaction does not mean one regulates the other; direction needs extra data.</li>
  <li><strong>Bitmap screenshots</strong>: journals will ask for a redraw. Export PDF/SVG from the start.</li>
</ul>

## 6. Exercises

<ol>
  <li>Import 20–50 DE genes into STRING and build networks at 0.4 and 0.7; compare edge counts.</li>
  <li>Map log2FC to colour and degree to size, then export a figure.</li>
  <li>Run NetworkAnalyzer; list the five highest-degree nodes.</li>
  <li>Find modules with MCODE, enrich the largest one with GO and interpret it.</li>
  <li>(Optional) Rank hubs with cytoHubba MCC and compare with the plain degree ranking.</li>
</ol>

## Further resources

<ul>
  <li><a href="https://cytoscape.org/documentation_users.html" target="_blank" rel="noopener">Cytoscape documentation</a></li>
  <li><a href="https://string-db.org/cgi/help" target="_blank" rel="noopener">STRING help</a></li>
  <li><a href="https://apps.cytoscape.org/apps/mcode" target="_blank" rel="noopener">MCODE</a></li>
  <li><a href="https://apps.cytoscape.org/apps/cytohubba" target="_blank" rel="noopener">cytoHubba</a></li>
</ul>
