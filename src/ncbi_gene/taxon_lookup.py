import logging
import os
from typing import Tuple

import requests
from functools import lru_cache

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@lru_cache(maxsize=128)
def get_taxon_name(taxon_id: str) -> str:
    """
    Fetch the scientific name for a given NCBI taxon ID via E-utilities.
    """
    ncbi_info = get_ncbi_access_data()
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "taxonomy",
        "id": taxon_id,
        "retmode": "json",
        "api_key": ncbi_info[0],
        "email": ncbi_info[1]
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    result = data.get("result", {})
    taxon_info = result.get(taxon_id)

    if taxon_info and "scientificname" in taxon_info:
        name = taxon_info["scientificname"]
        return name
    else:
        logger.warning(f"No scientific name found for taxon ID {taxon_id}")
        return ""

def get_ncbi_access_data() -> Tuple[str, str]:
    try:
        api_key = os.getenv("NCBI_API_KEY")
    except ValueError:
        api_key = None
        logger.debug("No NCBI_API_KEY provided. Will use none.")
    try:
        mail = os.getenv("NCBI_MAIL")
    except ValueError:
        mail = None
        logger.debug("No NCBI_MAIL provided. Will use none.")
    return api_key, mail