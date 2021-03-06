# Generated by Django 2.0.1 on 2018-08-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20180813_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='needknow',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='tellyou',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='老师告诉你能学到什么？'),
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=300, verbose_name='视频地址'),
        ),
    ]
