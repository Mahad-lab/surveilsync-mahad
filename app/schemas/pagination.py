from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# This PaginationParams model can be used to standardize the parameters for paginated endpoints.
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number, starting from 1")
    size: int = Field(
        10, ge=1, le=100, description="Number of items per page (max 100)"
    )

    class Config:
        json_schema_extra = {"example": {"page": 1, "size": 10}}


# This PaginationResponse model can be used to standardize the response format for paginated endpoints.
class PaginationResponse(BaseModel, Generic[T]):
    items: List[T] = Field(..., description="List of items in the current page")
    total: int = Field(..., description="Total number of items across all pages")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")

    class Config:
        json_schema_extra = {"example": {"items": [], "total": 5, "page": 1, "size": 10}}
