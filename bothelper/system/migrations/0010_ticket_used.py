# Generated by Django 2.2.5 on 2019-11-26 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_ticket_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='used',
            field=models.BooleanField(default=False, verbose_name='Использован'),
        ),
    ]