from pydantic import BaseModel, Field, PositiveFloat, field_validator
from typing import List
from typing_extensions import Annotated
from .payment import PaymentBaseModel, payment_models
from .menuitem import MenuItemModel
from bson.objectid import ObjectId as BsonObjectId


def _validate_payment_type(payment: PaymentBaseModel) -> PaymentBaseModel:
    '''
    Validate payment object type by checking if it is an instance of one of the payment models
    
    Args:
    payment (PaymentBaseModel): Payment Object
    
    Returns:
    PaymentBaseModel: Payment Object
    
    Raises:
    ValueError: If Payment Type is invalid
    '''
    for payment_model in payment_models():
        if isinstance(payment, payment_model):
            return payment
    
    raise ValueError("Invalid Payment Type")


class ItemOnOrderModel(BaseModel):
    ''' Item on Order Model '''
    item: MenuItemModel = Field(description="Item")
    quantity: int = Field(description="Quantity")
    price_at_order: PositiveFloat = Field(description="Price at Order")

class OrderModel(BaseModel):
    ''' Order Model '''
    id: str = Field(None, description="Order Id", alias="_id")
    total: PositiveFloat = Field(description="Total")
    created_at: str = Field(description="Created At")
    items: List[ItemOnOrderModel] = Field(description="Items")
    payment: Annotated[PaymentBaseModel, _validate_payment_type] = Field(description="Payment")

    @field_validator('id', mode='before')
    def _validate_id(cls, value):
        ''' Convert ObjectId to string '''
        if isinstance(value, BsonObjectId):
            return str(value)
        return value