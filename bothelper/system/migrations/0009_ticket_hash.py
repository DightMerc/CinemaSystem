# Generated by Django 2.2.5 on 2019-11-26 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_auto_20191110_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='hash',
            field=models.CharField(default='', max_length=400, verbose_name='Hash'),
        ),
    ]
