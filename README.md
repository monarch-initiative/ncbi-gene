# ncbi-gene

Koza ingest for NCBI Gene data, transforming gene information into Biolink model format.

## Data Source

[NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/) integrates information from a wide range of species. A record may include nomenclature, Reference Sequences (RefSeqs), maps, pathways, variations, phenotypes, and links to genome-, phenotype-, and locus-specific resources worldwide.

Data is downloaded from: `https://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz`

## Output

This ingest produces:
- **Gene nodes** - Gene entities with NCBI Gene IDs, symbols, names, and taxon information

### Biolink Properties Captured

- biolink:Gene
  - id
  - symbol
  - name
  - full_name
  - description
  - in_taxon
  - in_taxon_label
  - provided_by (["infores:ncbi-gene"])

### Postprocessing

Output is split by taxon into separate files in `output/by_taxon/`.

## Usage

```bash
# Install dependencies
just install

# Run full pipeline
just run

# Or run steps individually
just download      # Download gene_info data
just transform-all # Run Koza transform
just postprocess   # Split output by taxon
just test          # Run tests
```

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- [just](https://github.com/casey/just) command runner

## Environment Variables

- `NCBI_API_KEY` - NCBI API key for higher rate limits (optional)
- `NCBI_MAIL` - Email for NCBI E-utilities identification (optional)

## Citation

National Center for Biotechnology Information (NCBI)[Internet]. Bethesda (MD): National Library of Medicine (US), National Center for Biotechnology Information; [1988] - [cited 2024 Dec]. Available from: https://www.ncbi.nlm.nih.gov/

## License

BSD-3-Clause
