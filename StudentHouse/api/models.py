from django.db import models
from django.contrib.auth import get_user_model
from StudentHouse.organization.models import *
# Create your models here.

class TransactionRecord(models.Model):
    orderId = models.CharField(max_length=255)
    payed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="transaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default="NOT PAID") # this can be pending, paid, failed, cancelled, expired, refund
    metadata = models.CharField(max_length=5000, null=True, blank=True)

    @property
    def get_user(self):
        return self.payed_by.id if self.payed_by else None

# we should have one transaction many payments, so its okay to have foreignKey here
class PaymentRecord(models.Model):
    transaction = models.ForeignKey(TransactionRecord, on_delete=models.CASCADE, related_name="transaction", blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reference = models.CharField(max_length=1000, blank=True, null=True) # i think this come after someone pay for service so it should be coming from success payment
    mode = models.CharField(max_length=1000, blank=True, null=True, default='PAID')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="alielipia", null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="anaelipiwa", null=True, blank=True) # it only work if the one pay is mzazi
    amount = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def get_user(self):
        return self.user.id if self.user else None

    @property
    def get_transaction(self):
        if self.transaction:
            return {
                "id": self.transaction.id,
                "orderId": self.transaction.orderId,
                "amount": self.transaction.amount,
                "status": self.transaction.status,
                "user": self.transaction.get_user
            }
        return None

    @property
    def get_student(self):
        if self.student:
            return {
                "id": self.student.id,
            }
        return None
    