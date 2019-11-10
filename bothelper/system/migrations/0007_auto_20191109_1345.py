# Generated by Django 2.2.5 on 2019-11-09 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20191108_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionMovieDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Название')),
                ('date', models.DateField(verbose_name='День')),
                ('tickets', models.PositiveIntegerField(default=35, verbose_name='Количество билетов')),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='cinema',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='system.Cinema'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SessionDay',
        ),
        migrations.AddField(
            model_name='sessionmovieday',
            name='sessions',
            field=models.ManyToManyField(to='system.Session'),
        ),
    ]
