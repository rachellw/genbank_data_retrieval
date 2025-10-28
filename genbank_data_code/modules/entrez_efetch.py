# code written by Peter Freeman to retrieve data from Genbank using API

import requests
import xmltodict
from utils  import logger
class TranscriptIdError(Exception):
    """
    Custom exception raised when a transcript identifier does not meet the
    expected NCBI format requirements.
    """
    pass

def fetch_transcript_record(transcript_id):
    """
    Fetch a transcript record from the NCBI Nucleotide database using the
    Entrez EFetch API, and return the record as a Python dictionary
    (converted from XML).

    Parameters:
    transcript_id (str): A transcript accession with version number.
        Must start with NM_, NR_, XM_, or XR_ (e.g., "NM_000093.4").

    Returns:
    dict: A Python dictionary representation of the transcript record,
        parsed from the XML response.

    Raises:
    TranscriptIdError: If the transcript_id does not have the expected prefix
        or lacks a version number.
    requests.exceptions.RequestException: If there is a network or API error.
    """

    # Validate that the transcript ID has the expected RefSeq prefix
    if not transcript_id.startswith(("NM_", "NR_", "XM_", "XR_")):
        raise TranscriptIdError(
            f"Invalid transcript ID: {transcript_id}. "
            "Must start with NM_, NR_, XM_, or XR_."
        )

    # Validate that the transcript ID includes a version (e.g., ".3")
    if "." not in transcript_id:
        raise TranscriptIdError(
            f"Transcript ID {transcript_id} must include a version number "
            "(e.g., NM_000093.4)."
        )

    # Base URL for NCBI Entrez EFetch
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nucleotide",   # NCBI nucleotide database
        "id": transcript_id,  # transcript accession
        "retmode": "xml"      # request XML format for easier parsing
    }

    try:
        # Perform GET request to NCBI EFetch
        r = requests.get(url, params=params)
        r.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching transcript {transcript_id}: {e}")
        raise

    # Convert XML response to Python dict using xmltodict and strip out the GBSet/GBSeq wrapper
    return xmltodict.parse(r.text)['GBSet']['GBSeq']
