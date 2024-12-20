# Generated by Django 4.2 on 2023-06-05 09:23

from django.db import migrations, models
import django.db.models.deletion
import images.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('media_file', models.FileField(upload_to=images.models.upload_to)),
                ('AD_percent', models.FloatField(blank=True, default=0, null=True)),
                ('CN_percent', models.FloatField(blank=True, default=0, null=True)),
                ('MCI_percent', models.FloatField(blank=True, default=0, null=True)),
                ('predicted_class', models.CharField(blank=True, choices=[('CN', 'CN'), ('MCI', 'MCI'), ('AD', 'AD')], default='CN', max_length=4, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_studies', to='images.patient')),
            ],
        ),
    ]
