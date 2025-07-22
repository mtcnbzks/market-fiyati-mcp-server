from typing import List, Optional

from pydantic import BaseModel, Field


class ProductDepotInfo(BaseModel):
    depotId: str = Field(..., alias="depotId")
    depotName: str = Field(..., alias="depotName")
    price: float
    unitPrice: str = Field(..., alias="unitPrice")
    marketAdi: str = Field(..., alias="marketAdi")
    percentage: float
    longitude: float
    latitude: float
    indexTime: str = Field(..., alias="indexTime")


class ContentItem(BaseModel):
    id: str
    title: str
    brand: str
    imageUrl: str = Field(..., alias="imageUrl")
    refinedQuantityUnit: Optional[str] = Field(None, alias="refinedQuantityUnit")
    refinedVolumeOrWeight: Optional[str] = None
    categories: List[str]
    productDepotInfoList: List[ProductDepotInfo] = Field(
        ..., alias="productDepotInfoList"
    )


class Facet(BaseModel):
    name: str
    count: int


class FacetMap(BaseModel):
    sub_category: List[Facet]
    refined_quantity_unit: List[Facet]
    main_category: List[Facet]
    refined_volume_weight: List[Facet]
    brand: List[Facet]
    market_names: List[Facet]


class BaseApiResponse(BaseModel):
    """Tüm API yanıtları için temel model."""

    class Config:
        # Modelde tanımlanmayan alanlara izin ver
        extra = "allow"


class SearchResponse(BaseApiResponse):
    """/search uç noktası için yanıt modeli."""

    numberOfFound: int = Field(..., alias="numberOfFound")
    searchResultType: int = Field(..., alias="searchResultType")
    content: List[ContentItem]
    facetMap: Optional[FacetMap] = Field(None, alias="facetMap")


class SearchByIdentityResponse(BaseApiResponse):
    """/searchByIdentity uç noktası için yanıt modeli."""

    numberOfFound: int = Field(..., alias="numberOfFound")
    searchResultType: int = Field(..., alias="searchResultType")
    content: List[ContentItem]
    facetMap: Optional[FacetMap] = Field(None, alias="facetMap")


class SearchSimilarProductResponse(BaseApiResponse):
    """/searchSmilarProduct uç noktası için yanıt modeli."""

    numberOfFound: int = Field(..., alias="numberOfFound")
    searchResultType: int = Field(..., alias="searchResultType")
    content: List[ContentItem]
    facetMap: Optional[FacetMap] = Field(None, alias="facetMap")


class SearchRequestParams(BaseModel):
    keywords: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[int] = None


class SearchByIdentityRequestParams(BaseModel):
    identity: str
    identityType: str = "id"
    keywords: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[int] = None


# its not typo. original API uses "Smilar" instead of "Similar"
class SearchSmilarProductRequestParams(BaseModel):
    id: str
    keywords: str = Field(..., alias="keywords")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[int] = None
