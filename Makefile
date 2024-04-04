
.PHONY: download
download:
	downloader

.PHONY: transform
transform:
	koza transform --source ncbi_gene.yaml --target ncbi_gene.json

.PHONY: rdf
rdf:
	kgx transform -i tsv -f nt -d gz -o output/ncbi_gene_nodes.nt.gz output/ncbi_gene_nodes.tsv
