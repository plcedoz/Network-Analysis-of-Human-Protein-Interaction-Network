# Network Analysis of Human Protein Interaction Network

*Vincent Billaut, Pierre-Louis Cedoz, Matthieu de Rochemonteix*  
*CS224W - class project*

## List of resources

### Literature review
- *Controllability analysis of the directed human protein
interaction network identifies disease genes and
drug targets*, Vinayagam and al., 2016
  - `Controllability analysis of the directed human protein interaction network identifies disease genes and drug targets.pdf`
  - Supporting information, provided by the text authors: `supporting information.pdf`
  - "Datasets" links in the article only point to Excel files containing lists of references
- *Identification of new key genes for type 1 diabetes through
construction and analysis of protein–protein interaction
networks based on blood and pancreatic islet transcriptomes*, Safari-Alighiarloo and al., 2017
  - `jdb12483.pdf`
- *Network Robustness and Fragility: Percolation on Random Graphs*, Callaway and al., 2000
  - `PhysRebLett.85.5468.pdf`
- *A DIseAse MOdule Detection (DIAMOnD)
Algorithm Derived from a Systematic Analysis of
Connectivity Patterns of Disease Proteins in the
Human Interactome*, Ghiassian SD, Menche J, Barabási A-L
(2015)
  - `journal.pcbi.1004120.PDF`

### Data sources
Just found this [list of databases](https://www.ncbi.nlm.nih.gov/guide/all/) that might come in handy.  
Others mentioned in the first paper follow:
- PPI Networks
  - [STRING](http://string-db.org/)  
  - MINT: http://onlinelibrary.wiley.com/doi/10.1016/S0014-5793(01)03293-8/full
    - strange because the link to the db yields a 404
    - this is the article references in `Controllability`
- Disease-Protein Links
  - [GWAS](https://www.genome.gov/26525384/catalog-of-published-genomewide-association-studies/)
    - genome-wide association studies (GWAS)
    - "GWAS identify genomic regions but not specific coding genes that cause the disease"  
  - [NCG5.0](http://ncg.kcl.ac.uk/download.php)
    - Network of Cancer Genes
    - dump available
- Drug targets
  - [DrugBank](https://www.drugbank.ca/)
    - 77.4MB dump available
- Gene essentiality
  - [OGEE](http://ogee.medgenius.info/browse/)
    - dumps available
    - several cancer-related datasets
  - [EGGS](http://www.nmpdr.org/FIG/eggs.cgi)
    - data available [here](http://www.nmpdr.org/FIG/Html/CompleteSeedGenomes.html)
- Virus/Host molecular interactions
  - [VirHost](http://virhostnet.prabi.fr/)
    - dump available (**on** the "Download" button)
- [DirectedPPI](http://www.flyrnai.org/DirectedPPI/)
  - the database created by the authors of the `Controllability` paper
  - available on query (and _Integrated Node Information Table_ on download)

## Useful links

- [Course info](http://web.stanford.edu/class/cs224w/info.html), notably with instructions for the project
- [SNAP website](http://snap.stanford.edu/)
- [SNAP.py documentation](http://snap.stanford.edu/snappy/doc/index.html)
- [Networkx documentation](https://networkx.github.io/documentation/stable/)

- [Project report](https://www.overleaf.com/11646226vdtkjvrpjhjs#/44069796/)
