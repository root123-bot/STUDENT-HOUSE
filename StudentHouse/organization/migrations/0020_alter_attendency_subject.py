# Generated by Django 3.2 on 2023-04-08 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0019_attendency_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendency',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.subject'),
        ),
    ]
