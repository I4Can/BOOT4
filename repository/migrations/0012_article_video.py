# Generated by Django 2.1 on 2019-01-05 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0011_auto_20181027_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='video',
            field=models.FileField(blank=True, default='', null=True, upload_to='videos', verbose_name='视频'),
        ),
    ]