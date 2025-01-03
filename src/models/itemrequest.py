from pydantic import BaseModel, Field
from typing import Optional

class ItemRequestModel(BaseModel):
    ''' Model for item request filter '''
    name: Optional[str] = Field(None, title="Item name")
    category_id: Optional[int]  = Field(description="Category ID")
    price_from: Optional[float] = Field(description="Price From")
    price_to: Optional[float]   = Field(description="Price To")