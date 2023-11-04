# Generated by Django 3.2 on 2023-04-08 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0015_auto_20230408_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolExamTimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.CharField(max_length=50)),
                ('end_date', models.CharField(max_length=50)),
                ('is_finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='examtimetable',
            name='schoool_timetable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='darasa_timetable', to='organization.schoolexamtimetable'),
        ),
    ]
