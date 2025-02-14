from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid
from django.utils.timezone import now
from datetime import timedelta
import random
import string

# Create your models here.

UserModel = get_user_model()


class VoucherUploadTask(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField()
    original_filename = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("processed", "Processed"),
            ("failed", "Failed"),
        ],
        default="pending",
    )
    uploaded_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="tasks"
    )

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"UploadTask-{self.original_filename}"


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=256)
    order_value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.first_name}"


class Voucher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="vouchers"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_days = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    voucher_code = models.CharField(max_length=20, unique=True, editable=False)

    class Meta:
        db_table = "vouchers"
        indexes = [
            models.Index(fields=["voucher_code"]),
            models.Index(fields=["end_date"]),
        ]

    def __str__(self):
        return f"Voucher {self.voucher_code} - {self.amount} GHS"

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.valid_days)
        if not self.voucher_code:
            self.voucher_code = self.generate_voucher_code()

        super().save(*args, **kwargs)

    def generate_voucher_code(self):
        """Generates a unique voucher code with the format VOU-XXXXXX"""
        while True:
            code = "VOU-" + "".join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
            if not Voucher.objects.filter(voucher_code=code).exists():
                return code
