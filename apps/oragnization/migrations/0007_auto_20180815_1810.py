# Generated by Django 2.0.1 on 2018-08-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oragnization', '0006_teacher_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=0, verbose_name='年龄'),
        ),
    ]
