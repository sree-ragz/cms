# Generated by Django 4.1.7 on 2023-03-16 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prof', '0005_rename_remark_postersubmition_posterremark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postersubmition',
            old_name='posterremark',
            new_name='remark',
        ),
    ]