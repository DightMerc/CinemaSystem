# Generated by Django 2.2.5 on 2019-11-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20191016_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='photo',
            field=models.ImageField(default=None, upload_to='media/covers', verbose_name='Фото'),
            preserve_default=False,
        ),
    ]