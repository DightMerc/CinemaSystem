# Generated by Django 2.2.5 on 2019-10-09 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20191009_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('number', models.IntegerField(default=0)),
                ('text', models.TextField()),
            ],
        ),
    ]