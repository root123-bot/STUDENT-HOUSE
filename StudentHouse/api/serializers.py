from rest_framework import serializers
from .models import *

class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = [
            'id',
            'get_user',
            'start_date',
            'end_date',
            'reference',
            'mode',
            'get_user',
            'get_transaction',
            'amount',
            'get_student'
        ]

class TransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        mode = TransactionRecord
        fields = [
            'id',
            'orderId',
            'get_user',
            'amount',
            'created_at',
            'updated_at',
            'status'
        ]