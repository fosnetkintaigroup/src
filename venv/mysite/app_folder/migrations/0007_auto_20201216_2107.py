# Generated by Django 3.1.2 on 2020-12-16 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_folder', '0006_koutuhilist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='koutuhilist',
            name='customname',
        ),
        migrations.AddField(
            model_name='koutuhilist',
            name='homon',
            field=models.CharField(default='a', max_length=16, verbose_name='homon'),
        ),
        migrations.AddField(
            model_name='koutuhilist',
            name='tourokudate',
            field=models.DateField(default='2021-01-01', max_length=16, verbose_name='tourokudate'),
        ),
        migrations.AddField(
            model_name='koutuhilist',
            name='tourokukbn',
            field=models.CharField(default='申請済', max_length=16, verbose_name='shinseikbn'),
        ),
        migrations.AddField(
            model_name='koutuhilist',
            name='transport',
            field=models.IntegerField(default=0, verbose_name='route'),
        ),
    ]
