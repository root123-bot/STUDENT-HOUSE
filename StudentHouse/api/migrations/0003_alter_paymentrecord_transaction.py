# Generated by Django 3.2 on 2023-11-21 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_transactionrecord_transactionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrecord',
            name='transaction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='api.transactionrecord'),
        ),
    ]
