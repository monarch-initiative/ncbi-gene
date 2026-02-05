# ncbi-gene

This is a Koza ingest repository for transforming NCBI Gene data into Biolink model format.

## Project Structure

- `download.yaml` - Configuration for downloading NCBI gene_info data
- `src/` - Transform code and configuration
  - `transform.py` / `transform.yaml` - Main transform for NCBI genes
  - `taxon_lookup.py` - Helper module for fetching taxon names via NCBI E-utilities
- `tests/` - Unit tests for transforms
- `output/` - Generated nodes and edges (gitignored)
- `data/` - Downloaded source data (gitignored)

## Key Commands

- `just run` - Full pipeline (download -> transform -> postprocess)
- `just download` - Download NCBI gene_info data
- `just transform-all` - Run all transforms
- `just postprocess` - Split output by taxon
- `just test` - Run tests

## Postprocessing

This ingest includes a postprocessing step to split the output nodes file by taxon:
```bash
uv run koza split output/ncbi_gene_nodes.tsv in_taxon --remove-prefixes --output-dir output/by_taxon
```

This creates separate files per species in `output/by_taxon/`.

## Environment Variables

The taxon lookup module uses NCBI E-utilities and can be configured with:
- `NCBI_API_KEY` - NCBI API key for higher rate limits
- `NCBI_MAIL` - Email for NCBI E-utilities identification
