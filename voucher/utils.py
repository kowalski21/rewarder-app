from decimal import Decimal
from uuid import uuid4 as u4
import csv
from collections import namedtuple
from datetime import datetime, timedelta
from .models import VoucherUploadTask, Customer, Voucher
from .validator import VoucherRowModel
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

VOUCHER_RULES = [
    {"min_value": Decimal("10000"), "amount": Decimal("1000"), "validity_days": 10},
    {"min_value": Decimal("5000"), "amount": Decimal("500"), "validity_days": 5},
    {"min_value": Decimal("1000"), "amount": Decimal("100"), "validity_days": 1},
]

VoucherRule = namedtuple("VoucherRule", ["amount", "validity_days", "is_applicable"])


def get_voucher_amount(order_value: Decimal) -> VoucherRule:
    for rule in VOUCHER_RULES:
        if order_value >= rule["min_value"]:
            logger.info("Voucher Rule found")
            return VoucherRule(rule["amount"], rule["validity_days"], True)
    return VoucherRule(Decimal("0"), 0, False)


def stream_csv_rows(voucher_task: VoucherUploadTask):
    with voucher_task.csv_file.open("r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def process_data(row: dict, upload_task_id: int):
    customer_id = row.get("Customer ID", None)
    first_name = row.get("Customer First Name", None)
    order_value = row.get("Order Value", 0)
    try:
        payload = VoucherRowModel(
            first_name=first_name, customer_id=customer_id, order_value=order_value
        )
        # print(payload)
        voucher_info = get_voucher_amount(payload.order_value)
        # print(voucher_info)
        if not voucher_info.is_applicable:
            return
        customer, _ = Customer.objects.update_or_create(
            id=customer_id,
            defaults={"first_name": first_name, "order_value": Decimal(order_value)},
        )
        voucher = Voucher.objects.create(
            customer=customer,
            amount=voucher_info.amount,
            start_date=datetime.now(),
            valid_days=voucher_info.validity_days,
            end_date=datetime.now() + timedelta(days=voucher_info.validity_days),
        )

    except ValidationError as e:
        # print(e.json()[0])
        logger.error(f"UploadTaskID-{upload_task_id},{row},{e.json()}")


def process_csv(upload_task_id: int):
    print(upload_task_id)
    voucher_task = VoucherUploadTask.objects.get(id=upload_task_id)
    for row in stream_csv_rows(voucher_task):
        process_data(row, upload_task_id)
