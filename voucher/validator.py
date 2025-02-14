from pydantic import BaseModel, Field
from decimal import Decimal


class VoucherRowModel(BaseModel):
    first_name: str
    customer_id: int
    order_value: Decimal = Field(max_digits=10, decimal_places=2)
