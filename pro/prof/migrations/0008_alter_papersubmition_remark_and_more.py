# Generated by Django 4.1.7 on 2023-03-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prof', '0007_rename_remark_postersubmition_posterremark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papersubmition',
            name='remark',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='postersubmition',
            name='posterremark',
            field=models.TextField(max_length=1000),
        ),
    ]
