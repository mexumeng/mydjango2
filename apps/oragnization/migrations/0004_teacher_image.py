# Generated by Django 2.0.1 on 2018-08-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oragnization', '0003_auto_20180802_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='org/%Y/%m', verbose_name='讲师头像'),
        ),
    ]
