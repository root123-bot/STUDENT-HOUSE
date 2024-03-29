# Generated by Django 3.2 on 2023-04-08 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0014_darasa_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='darasa',
            name='students',
        ),
        migrations.AddField(
            model_name='student',
            name='darasa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.darasa'),
        ),
        migrations.AddField(
            model_name='student',
            name='mkondo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.mkondo'),
        ),
    ]
