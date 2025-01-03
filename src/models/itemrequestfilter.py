from pydantic import BaseModel, Field, model_validator, PositiveFloat
from typing import Optional

class ItemRequestFilterModel(BaseModel):
    ''' Model for item request filter '''
    name: Optional[str]                 = Field(None, title="Item name")
    category_id: Optional[int]          = Field(description="Category ID")
    price_from: Optional[PositiveFloat] = Field(description="Price From")
    price_to: Optional[PositiveFloat]   = Field(description="Price To")
    
    # Validate attributes
    @model_validator(mode="after")
    def validate_att(self):
        # Check the price range if both are provided
        if self.price_from and self.price_to and self.price_from > self.price_to:
            raise ValueError("Price From should be less than Price To")
        return self
    
    def as_query(self):
        ''' Convert the model to a query dictionary '''
        query = {}
        
        if self.name:
            query["name"] = {"$regex": self.name, "$options": "i"}
        if self.category_id:
            query["category_id"] = self.category_id
            
        # If both price_from and price_to are provided, create a range query
        if self.price_from and self.price_to:
            query["price"] = {"$gte": self.price_from, "$lte": self.price_to}
            
        elif self.price_from:
            query["price"] = {"$gte": self.price_from}
        elif self.price_to:
            query["price"] = {"$lte": self.price_to}
            
        return query
    