from config.celery import app
import logging
from .utils import process_csv
from .models import VoucherUploadTask

logger = logging.getLogger(__name__)


@app.task
def process_csv_file(file_id: int, file_name: str):
    logger.info(f"Processing File- {file_id},{file_name}")
    process_csv(file_id)
    VoucherUploadTask.objects.filter(id=file_id).update(id=file_id, status="completed")
    logger.info("Completed")
