from pydantic import BaseModel, Field

class CategoryModel(BaseModel):
    ''' Category Model '''
    id: int       = Field(description="Category ID")
    name: str     = Field(description="Category Name")
    image_id: str = Field(description="Image ID")