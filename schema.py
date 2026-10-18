from pydantic import BaseModel, ConfigDict, Field


class Book(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    title: str = Field(min_length=1)
    price_gbp: float = Field(gt=0, lt=1000)
    stock: int = Field(ge=0)
    rating: int = Field(ge=1, le=5)
    upc: str = Field(pattern=r"^[0-9a-f]{16}$")
    url: str = Field(pattern=r"^https://books\.toscrape\.com/catalogue/[^/]+/index\.html$")