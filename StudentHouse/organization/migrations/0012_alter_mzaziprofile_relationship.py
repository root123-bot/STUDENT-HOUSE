# Generated by Django 3.2 on 2023-04-06 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0011_mzaziprofile_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mzaziprofile',
            name='relationship',
            field=models.CharField(default='Parent', max_length=500),
        ),
    ]
