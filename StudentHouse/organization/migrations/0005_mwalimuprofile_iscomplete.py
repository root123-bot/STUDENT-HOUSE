# Generated by Django 3.2 on 2023-03-27 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20230327_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='mwalimuprofile',
            name='isComplete',
            field=models.BooleanField(default=False),
        ),
    ]
