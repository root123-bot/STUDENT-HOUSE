# Generated by Django 3.2 on 2023-03-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20230325_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mwalimuprofile',
            name='register_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]