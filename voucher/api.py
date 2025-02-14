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
from accounts.authenticate import AuthenticationBearer

router = Router(auth=AuthenticationBearer())


@router.post("/upload-csv")
def upload_csv(request, file: UploadedFile = File(...)):
    user = request.auth
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file.name}"
    file_record = storage.save(file_name, file)
    upload_task = VoucherUploadTask.objects.create(
        csv_file=file_record, original_filename=file.name, uploaded_by=user
    )
    task = process_csv_file.delay(upload_task.id, file_name)
    return Munch(
        message="File uploaded", task_id=upload_task.id, celery_task_id=task.id
    )
