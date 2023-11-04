# Generated by Django 3.2 on 2023-05-04 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0026_classtimetable_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='matukio',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matukio', to='organization.instituteprofile'),
        ),
        migrations.AlterField(
            model_name='darasa',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='organization.instituteprofile'),
        ),
    ]
