from ninja import Router, File, UploadedFile, NinjaAPI, Form
from munch import Munch
from django.core.files.storage import default_storage as storage
from datetime import datetime
from .models import VoucherUploadTask, Voucher, Customer
from .schema import (
    CustomerSchema,
    CustomersListSchema,
    VoucherListSchema,
    VoucherSchema,
)
from .tasks import process_csv_file
from .utils import process_csv


router = Router()


@router.post("/upload-csv")
def upload_csv(request, file: UploadedFile = File(...)):
    print(file.name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file.name}"
    file_record = storage.save(file_name, file)
    upload_task = VoucherUploadTask.objects.create(
        csv_file=file_record, original_filename=file.name
    )
    print(upload_task.id)
    task = process_csv_file.delay(upload_task.id, file_name)
    # pass it to celery task
    return Munch(
        message="File uploaded", task_id=upload_task.id, celery_task_id=task.id
    )
