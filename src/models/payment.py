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


class CardPaymentModel(PaymentBaseModel):
    ''' Payment Card Model '''
    card_number: str = Field(description="Card Number")
    card_holder: str = Field(description="Card Holder")
    expiration_date: str = Field(description="Expiration Date")
    cvv: str = Field(description="CVV")


class PixPaymentModel(PaymentBaseModel):
    ''' Payment PIX Model '''
    client_name: str = Field(description="Client Name")
    client_id: str = Field(description="Client Id")
    pix_code: str = Field(description="PIX EMV Code")
    created_at: str = Field(description="Created At")
    expiration_date: str = Field(description="Expiration Date")
