# Generated by Django 3.2 on 2023-03-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituteprofile',
            name='register_date',
            field=models.CharField(default=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='instituteprofile',
            name='school_level',
            field=models.CharField(default=True, max_length=50, null=True),
        ),
    ]
