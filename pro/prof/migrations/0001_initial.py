# Generated by Django 4.1.7 on 2023-03-05 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=225)),
                ('designation', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='images')),
                ('ph_no', models.CharField(max_length=12)),
                ('is_author', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(default=models.CharField(max_length=200, null=True), editable=False, max_length=100)),
                ('modified_on', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.CharField(default=models.CharField(max_length=200, null=True), editable=False, max_length=100)),
                ('Rstatus', models.CharField(default='v', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaperSubmition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('papername', models.CharField(max_length=200)),
                ('abstract', models.CharField(max_length=200)),
                ('paperfile', models.FileField(upload_to='uploads/')),
                ('track', models.CharField(default='h', max_length=200, null=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
