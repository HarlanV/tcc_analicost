# Generated by Django 3.2.8 on 2022-02-28 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opex', '0002_auto_20220228_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='opexauxiliatefactor',
            name='crm_calculated',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='opexauxiliatefactor',
            name='revenue_calculated',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='opexauxiliatefactor',
            name='salvage_calculated',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
