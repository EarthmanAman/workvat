# Generated by Django 2.2.5 on 2019-09-30 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0006_userassignment_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassignment',
            name='expectedDat',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
