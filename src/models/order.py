from pydantic import BaseModel, Field
from typing import List, Union
from typing_extensions import Annotated
from datetime import datetime
from .payment import PaymentBaseModel, payment_models
from .menuitem import MenuItemModel

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

class OrderModel(BaseModel):
    ''' Order Model '''
    total: float = Field(description="Total")
    created_at: str = Field(description="Created At")
    items: List[ItemOnOrderModel] = Field(description="Items")
    payment: Annotated[PaymentBaseModel, _validate_payment_type] = Field(description="Payment")

class StoredOrderModel(OrderModel):
    ''' Stored Order Model '''
    id: int = Field(description="ID")