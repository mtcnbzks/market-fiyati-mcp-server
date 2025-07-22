import json
import logging
from typing import Any, Optional, Type, TypeVar

import requests
from pydantic import BaseModel, ValidationError

from .models import (
    SearchByIdentityRequestParams,
    SearchByIdentityResponse,
    SearchRequestParams,
    SearchResponse,
    SearchSimilarProductResponse,
    SearchSmilarProductRequestParams,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://api.marketfiyati.org.tr/api/v2"
HEADERS = {
    "cache-control": "no-cache",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
}
REQUEST_TIMEOUT = 10  # seconds

# Generic TypeVar for Pydantic models
T = TypeVar("T", bound=BaseModel)


def _make_request(
    endpoint: str, payload_data: dict[str, Any], response_model: Type[T]
) -> Optional[T]:
    """
    Sends a POST request to the specified API endpoint and validates the response.

    Args:
        endpoint: The API endpoint to send the request to.
        payload_data: The dictionary to be sent as JSON payload.
        response_model: The Pydantic model to validate the response against.

    Returns:
        A validated Pydantic model instance or None if an error occurs.
    """
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.post(
            url, headers=HEADERS, data=json.dumps(payload_data), timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        return response_model.model_validate(response.json())
    except requests.exceptions.Timeout:
        logging.error(f"Request to {url} timed out.")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request error for endpoint '{endpoint}': {e}")
    except ValidationError as e:
        logging.error(f"Data validation error for endpoint '{endpoint}': {e}")
    return None


def search(
    params: SearchRequestParams,
) -> Optional[SearchResponse]:
    """
    Anahtar kelimelere göre ürün arar.
    """
    return _make_request(
        endpoint="search",
        payload_data=params.model_dump(by_alias=True, exclude_none=True),
        response_model=SearchResponse,
    )


def search_by_identity(
    params: SearchByIdentityRequestParams,
) -> Optional[SearchByIdentityResponse]:
    """
    Kimliğe göre ürün arar.
    """
    return _make_request(
        endpoint="searchByIdentity",
        payload_data=params.model_dump(by_alias=True, exclude_none=True),
        response_model=SearchByIdentityResponse,
    )


def search_similar_product(
    params: SearchSmilarProductRequestParams,
) -> Optional[SearchSimilarProductResponse]:
    """
    Benzer ürünleri arar.
    """
    return _make_request(
        endpoint="searchSmilarProduct",  # yes, this is a typo in the original API
        payload_data=params.model_dump(by_alias=True, exclude_none=True),
        response_model=SearchSimilarProductResponse,
    )
