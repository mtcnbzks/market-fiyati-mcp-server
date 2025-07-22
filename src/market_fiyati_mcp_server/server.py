import logging
from typing import Any, Dict, List, Optional, Tuple

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from .market_fiyati_client.api_client import (
    search,
    search_by_identity,
    search_similar_product,
)
from .market_fiyati_client.models import (
    SearchByIdentityRequestParams,
    SearchByIdentityResponse,
    SearchRequestParams,
    SearchResponse,
    SearchSimilarProductResponse,
    SearchSmilarProductRequestParams,
)

# ---------- logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("market_fiyati_server")

# ---------- server ----------
mcp = FastMCP("Market Fiyatı")


# ---------- tools ----------
@mcp.tool(
    name="search_product",
    description="Search for products matching given keywords.",
    title="Search product",
)
def search_product(
    keywords: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    distance: Optional[int] = None,
) -> Tuple[List[TextContent], Optional[SearchResponse]]:
    """
    Search for products matching given keywords.
    Optionally restrict results by geo-coordinates (latitude, longitude, distance in meters).
    Returns:
        - A human-readable summary (`List[TextContent]`)
        - Full structured API response (`SearchResponse`) for downstream processing
    """
    p: Dict[str, Any] = {"keywords": keywords}
    if latitude is not None:
        p["latitude"] = latitude
    if longitude is not None:
        p["longitude"] = longitude
    if distance is not None:
        p["distance"] = distance

    logger.info("search_product %s", p)
    resp = search(SearchRequestParams(**p))

    if resp is None or not resp.content:
        return [TextContent(type="text", text="No results found.")], resp

    top = resp.content[0]
    msg = f"Top match: {top.title} ({top.brand}) — {resp.numberOfFound:,} result(s)."
    return [TextContent(type="text", text=msg)], resp


@mcp.tool(
    name="search_product_by_identity",
    description="Retrieve product information by a unique identity (e.g., barcode or internal ID).",
    title="Search product by identity",
)
def search_product_by_identity(
    identity: str,
    identityType: str = "id",
    keywords: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    distance: Optional[int] = None,
) -> Tuple[List[TextContent], Optional[SearchByIdentityResponse]]:
    """
    Retrieve product information by a unique identity (e.g., barcode or internal ID).
    Supports optional keyword filtering and geo-based narrowing of results.
    """
    p: Dict[str, Any] = {"identity": identity, "identityType": identityType}
    if keywords is not None:
        p["keywords"] = keywords
    if latitude is not None:
        p["latitude"] = latitude
    if longitude is not None:
        p["longitude"] = longitude
    if distance is not None:
        p["distance"] = distance

    logger.info("search_product_by_identity %s", p)
    resp = search_by_identity(SearchByIdentityRequestParams(**p))

    if resp is None or not resp.content:
        return [TextContent(type="text", text="No products found.")], resp

    top = resp.content[0]
    msg = (
        f"Found {resp.numberOfFound:,} item(s) for '{identity}'. "
        f"Example: {top.title} ({top.brand})."
    )
    return [TextContent(type="text", text=msg)], resp


@mcp.tool(
    name="search_similar_products",
    description="Find products similar to a reference item ID, optionally refined by keywords and geographic constraints.",
    title="Search similar products",
)
def search_similar_products(
    id: str,
    keywords: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    distance: Optional[int] = None,
) -> Tuple[List[TextContent], Optional[SearchSimilarProductResponse]]:
    """
    Find products similar to a reference item ID, optionally refined by keywords
    and geographic constraints.
    """
    p: Dict[str, Any] = {"id": id, "keywords": keywords}
    if latitude is not None:
        p["latitude"] = latitude
    if longitude is not None:
        p["longitude"] = longitude
    if distance is not None:
        p["distance"] = distance

    logger.info("search_similar_products %s", p)
    resp = search_similar_product(SearchSmilarProductRequestParams(**p))

    if resp is None or not resp.content:
        return [TextContent(type="text", text="No similar products found.")], resp

    top = resp.content[0]
    msg = (
        f"{resp.numberOfFound:,} similar product(s) found. "
        f"Closest match: {top.title} ({top.brand})."
    )
    return [TextContent(type="text", text=msg)], resp


def main():
    """
    Main entry point to start the MCP server.
    """
    mcp.run()
