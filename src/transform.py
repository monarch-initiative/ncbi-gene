import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import koza
from biolink_model.datamodel.pydanticmodel_v2 import Gene

from taxon_lookup import get_taxon_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@koza.transform_record()
def transform(koza, row: dict) -> list[Gene]:
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
    return [gene]
