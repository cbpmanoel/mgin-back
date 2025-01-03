from pydantic import BaseModel, Field, PositiveFloat

class MenuItemModel(BaseModel):
    ''' Menu Item Model '''
    cateory_id: int      = Field(description="Category ID")
    id: int              = Field(description="Menu Item ID")
    name: str            = Field(description="Menu Item Name")
    image_id: str        = Field(description="Image ID")
    price: PositiveFloat = Field(description="Price")
