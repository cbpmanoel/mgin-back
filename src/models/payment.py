from pydantic import BaseModel, Field, PositiveFloat
from enum import Enum

class PaymentType(str, Enum):
    ''' Payment Type Enum '''
    CARD = "card"
    PIX = "pix"

class PaymentBaseModel(BaseModel):
    ''' Payment Model '''
    type: PaymentType = Field(description="Payment Type, can be card or PIX")
    amount: PositiveFloat = Field(description="Amount")


class PaymentCardModel(PaymentBaseModel):
    ''' Payment Card Model '''
    card_number: str = Field(description="Card Number")
    card_holder: str = Field(description="Card Holder")
    expiration_date: str = Field(description="Expiration Date")
    cvv: str = Field(description="CVV")


class PaymentPixModel(PaymentBaseModel):
    ''' Payment PIX Model '''
    buyer_name: str = Field(description="Buyer Name")
    key: str = Field(description="PIX Key")
    expiration_date: str = Field(description="Expiration Date")


def payment_models():
    '''
    Return the valid payment models

    Returns:
    dict: Payment Models
    '''
    return PaymentCardModel, PaymentPixModel