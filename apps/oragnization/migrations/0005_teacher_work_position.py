# Generated by Django 2.0.1 on 2018-08-13 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oragnization', '0004_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(default='', max_length=30, verbose_name='公司职位'),
        ),
    ]
