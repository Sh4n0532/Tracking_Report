# Generated by Django 4.2.1 on 2023-05-14 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_quotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='quotation', to='app.project'),
        ),
    ]