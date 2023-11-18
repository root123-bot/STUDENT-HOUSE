from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class TransactionRecord(models.Model):
    transactionId = models.CharField(max_length=255)
    orderId = models.CharField(max_length=255)
    payed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="transaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default="NOT PAID") # this can be pending, paid, failed, cancelled, expired, refund

class PaymentRecord(models.Model):
    transaction = models.OneToOneField(TransactionRecord, on_delete=models.CASCADE, related_name="transaction")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reference = models.CharField(max_length=1000) # i think this come after someone pay for service so it should be coming from success payment