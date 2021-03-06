# Generated by Django 3.1.2 on 2020-12-19 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_folder', '0007_auto_20201216_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='syain_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('syain_cd', models.CharField(max_length=16, verbose_name='syain_cd')),
                ('syain_name', models.CharField(max_length=16, verbose_name='syain_name')),
                ('password', models.CharField(max_length=16, verbose_name='password')),
            ],
            options={
                'db_table': 'syain_info',
            },
        ),
        migrations.CreateModel(
            name='trans_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tourokukbn', models.CharField(default='申請済', max_length=16, verbose_name='shinseikbn')),
                ('tourokuno', models.CharField(default='0001', max_length=16, verbose_name='tourokunon')),
                ('syaincd', models.CharField(default='0001', max_length=16, verbose_name='syaincd')),
                ('syainname', models.CharField(default='佐藤', max_length=16, verbose_name='syaincd')),
                ('tourokudate', models.DateField(default='2021-01-01', max_length=16, verbose_name='tourokudate')),
                ('startdate', models.DateField(default='2021-01-01', max_length=16, verbose_name='startdate')),
                ('enddate', models.DateField(default='2021-01-01', max_length=16, verbose_name='enddate')),
                ('homon', models.CharField(default='a', max_length=16, verbose_name='homon')),
                ('kamoku', models.CharField(default='交通費', max_length=16, verbose_name='kamoku')),
                ('syudan', models.CharField(default='電車', max_length=16, verbose_name='syudan')),
                ('transport', models.IntegerField(default=0, verbose_name='transport')),
                ('k_seikyu', models.CharField(default='0', max_length=2, verbose_name='transport')),
                ('customname', models.CharField(default=0, max_length=16, verbose_name='customname')),
                ('seisan_kbn', models.CharField(default='現金', max_length=16, verbose_name='seisan_kbn')),
            ],
            options={
                'db_table': 'trans_info',
            },
        ),
        migrations.DeleteModel(
            name='koutuhilist',
        ),
    ]
