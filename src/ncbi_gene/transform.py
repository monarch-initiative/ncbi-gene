import logging

from koza.cli_utils import get_koza_app
from biolink_model.datamodel.pydanticmodel_v2 import Gene

from ncbi_gene.taxon_lookup import get_taxon_name

koza_app = get_koza_app("ncbi_gene")  # depending on the ingest name here is unfortunate
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

while (row := koza_app.get_row()) is not None:
    if "object_taxon_label" not in row or not row["object_taxon_label"]:
        in_taxon_label = get_taxon_name(row["tax_id"])
        row["object_taxon_label"] = in_taxon_label
    gene = Gene(
                id='NCBIGene:' + row["GeneID"],
                symbol=row["Symbol"],
                name=row["Symbol"],
                full_name=row["Full_name_from_nomenclature_authority"],
                description=row["description"],
                in_taxon=['NCBITaxon:' + row["tax_id"]],
                provided_by=["infores:ncbi-gene"],
                in_taxon_label=row["object_taxon_label"]
            )
    koza_app.write(gene)
