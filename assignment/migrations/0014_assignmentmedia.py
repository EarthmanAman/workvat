# Generated by Django 2.2.5 on 2019-10-08 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0013_userassignment_is_sample'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('is_complete', models.BooleanField(default=False)),
                ('userAssignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.UserAssignment')),
            ],
        ),
    ]
