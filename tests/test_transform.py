"""
An example test file for the transform script.

It uses pytest fixtures to define the input data and the mock koza transform.
The test_example function then tests the output of the transform script.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""
from pathlib import Path

import pytest

from biolink_model.datamodel.pydanticmodel_v2 import Gene

from koza.utils.testing_utils import mock_koza

# Define the ingest name and transform script path
INGEST_NAME = "ncbi_gene"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRANSFORM_SCRIPT = str(PROJECT_ROOT / "src" / "ncbi_gene" / "transform.py")


# Define an example row to test (as a dictionary)
@pytest.fixture
def example_row():
    return {
        "tax_id": "24",
        "GeneID": "77267469",
        "Symbol": "gyrB",
        "LocusTag": "N5094_RS00020",
        "Synonyms": "N5094_00020",
        "dbXrefs": "-",
        "chromosome": "-",
        "map_location": "-",
        "description": "DNA topoisomerase (ATP-hydrolyzing) subunit B",
        "type_of_gene": "protein-coding",
        "Symbol_from_nomenclature_authority": "-",
        "Full_name_from_nomenclature_authority": "-",
        "Nomenclature_status": "-",
        "Other_designations": "DNA topoisomerase (ATP-hydrolyzing) subunit B",
        "Modification_date": "20230411",
        "Feature_type": "-",
    }


# Define the mock koza transform
@pytest.fixture
def mock_transform(mock_koza, example_row):
    # Returns [entity_a, entity_b, association] for a single row
    return mock_koza(
        INGEST_NAME,
        example_row,
        TRANSFORM_SCRIPT,
    )


# Or for multiple rows
# @pytest.fixture
# def mock_transform_multiple_rows(mock_koza, example_list_of_rows):
#     # Returns concatenated list of [entity_a, entity_b, association]
#     # for each row in example_list_of_rows
#     return mock_koza(
#         INGEST_NAME,
#         example_list_of_rows,
#         TRANSFORM_SCRIPT,
#     )


# Test the output of the transform


@pytest.fixture
def expected():
    return Gene(
        id="NCBIGene:77267469",
        category=["biolink:Gene"],
        name="gyrB",
        description="DNA topoisomerase (ATP-hydrolyzing) subunit B",
        provided_by=["infores:ncbi-gene"],
        full_name="-",
        in_taxon=["NCBITaxon:24"],
        symbol="gyrB",
        in_taxon_label="Shewanella putrefaciens"
    )

@pytest.fixture(autouse=True)
def mock_taxon_lookup(monkeypatch):
    def fake_taxon_name(tax_id):
        return "Shewanella putrefaciens"
    monkeypatch.setattr("ncbi_gene.taxon_lookup.get_taxon_name", fake_taxon_name)


def test_single_row(mock_transform, expected):
    assert len(mock_transform) == 1
    entity = mock_transform[0]
    assert entity
    assert entity.name == "gyrB"
    assert entity == expected
