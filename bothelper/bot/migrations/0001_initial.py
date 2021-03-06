# Generated by Django 2.2.5 on 2019-09-16 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaySystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegramId', models.PositiveIntegerField(verbose_name='Telegram ID')),
                ('fullName', models.CharField(default='', max_length=255, verbose_name='Полное имя')),
                ('username', models.CharField(default='', max_length=255, null=True, verbose_name='Username')),
                ('phone', models.PositiveIntegerField(blank=True, null=True, verbose_name='Phone Number')),
                ('language', models.CharField(default='RU', max_length=5, verbose_name='Язык')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Название')),
                ('token', models.CharField(default='', max_length=255, verbose_name='Токен')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Название')),
                ('paySystem', models.ManyToManyField(to='bot.PaySystem')),
                ('telegramBotToken', models.ForeignKey(on_delete='Токен', to='bot.Token')),
            ],
        ),
        migrations.AddField(
            model_name='paysystem',
            name='paySystemToken',
            field=models.ForeignKey(on_delete='Токен', to='bot.Token'),
        ),
    ]
