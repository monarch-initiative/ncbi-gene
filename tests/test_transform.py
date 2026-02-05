"""
Test file for the transform script.

Uses the KozaRunner pattern with PassthroughWriter for testing transforms.
See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""
import importlib.util
from pathlib import Path

import pytest

from biolink_model.datamodel.pydanticmodel_v2 import Gene
from koza.runner import KozaRunner, PassthroughWriter, load_transform


# Define the transform script path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRANSFORM_SCRIPT = PROJECT_ROOT / "src" / "transform.py"


def load_module_from_path(path: Path):
    """Load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_transform(rows: list[dict]) -> list:
    """Run the transform on a list of input rows and return the output entities."""
    module = load_module_from_path(TRANSFORM_SCRIPT)
    hooks = load_transform(module)
    writer = PassthroughWriter()
    runner = KozaRunner(
        data=iter(rows),
        writer=writer,
        hooks=hooks,
        base_directory=TRANSFORM_SCRIPT.parent,
    )
    runner.run()
    return writer.data


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
    monkeypatch.setattr("taxon_lookup.get_taxon_name", fake_taxon_name)


def test_single_row(example_row, expected):
    result = run_transform([example_row])
    assert len(result) == 1
    entity = result[0]
    assert entity
    assert entity.name == "gyrB"
    assert entity == expected
