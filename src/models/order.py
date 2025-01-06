from pydantic import BaseModel, Field, PositiveFloat, field_validator
from typing import List, Union
from .payment import CardPaymentModel, PixPaymentModel
from .menuitem import MenuItemModel
from bson.objectid import ObjectId as BsonObjectId

class ItemOnOrderModel(BaseModel):
    ''' Item on Order Model '''
    item: MenuItemModel = Field(description="Item")
    quantity: int = Field(description="Quantity")

class OrderModel(BaseModel):
    ''' Order Model '''
    id: str = Field(None, description="Order Id", alias="_id")
    total: PositiveFloat = Field(description="Total")
    created_at: str = Field(description="Created At")
    items: List[ItemOnOrderModel] = Field(description="Items")
    payment: Union[CardPaymentModel, PixPaymentModel] = Field(description="Payment")

    @field_validator('id', mode='before')
    def _validate_id(cls, value):
        ''' Convert ObjectId to string '''
        if isinstance(value, BsonObjectId):
            return str(value)
        return value