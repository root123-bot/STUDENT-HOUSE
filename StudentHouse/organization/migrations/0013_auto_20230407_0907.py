# Generated by Django 3.2 on 2023-04-07 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0012_alter_mzaziprofile_relationship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='darasa',
            name='subclass',
        ),
        migrations.AddField(
            model_name='mkondo',
            name='darasa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mkondo', to='organization.darasa'),
        ),
    ]
