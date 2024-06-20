from koza.cli_utils import get_koza_app
from biolink_model.datamodel.pydanticmodel_v2 import Gene

koza_app = get_koza_app("ncbi_gene")  # depending on the ingest name here is unfortunate

while (row := koza_app.get_row()) is not None:

    gene = Gene(
        id='NCBIGene:' + row["GeneID"],
        symbol=row["Symbol"],
        name=row["Symbol"],
        full_name=row["Full_name_from_nomenclature_authority"],
        description=row["description"],
        in_taxon=['NCBITaxon:' + row["tax_id"]],
        provided_by=["infores:ncbi-gene"]
    )

    koza_app.write(gene)
