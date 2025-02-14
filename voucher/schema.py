from .models import Voucher, Customer
from ninja import ModelSchema
from typing import List


class VoucherSchema(ModelSchema):
    class Meta:
        model = Voucher
        fields = "__all__"


class CustomerSchema(ModelSchema):
    vouchers: List[VoucherSchema]

    class Meta:
        model = Customer
        fields = "__all__"


CustomersListSchema = List[CustomerSchema]
VoucherListSchema = List[VoucherSchema]
