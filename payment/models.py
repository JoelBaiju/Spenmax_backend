from django.db import models
from user.models import CustomUser
from django.utils import timezone
from shop.models import PackageOption

class RazorpayPayment(models.Model):
    class PaymentStatus(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Success'
        PENDING = 'PENDING', 'Pending'
        FAILED = 'FAILED', 'Failed'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name = "user_transaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider_order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    signature_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    date_of_payment = models.DateTimeField(default=timezone.now)
    package_option = models.ForeignKey(PackageOption, on_delete=models.CASCADE )