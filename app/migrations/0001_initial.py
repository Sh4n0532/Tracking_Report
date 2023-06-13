# Generated by Django 4.2.1 on 2023-05-11 02:34

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
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientName', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phoneNo', models.CharField(blank=True, max_length=15, null=True)),
                ('status', models.BooleanField(default=True)),
                ('createdOn', models.DateTimeField(blank=True, null=True)),
                ('updatedOn', models.DateTimeField(blank=True, null=True)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='clientCreated', to=settings.AUTH_USER_MODEL)),
                ('updatedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='clientUpdated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]