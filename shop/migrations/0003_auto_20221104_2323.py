# Generated by Django 2.0.13 on 2022-11-04 15:23

from django.db import migrations, models
import media.storage


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20221104_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='bannerImg',
            field=models.ImageField(default='', storage=media.storage.ImageStorage(), upload_to='banner/', verbose_name='广告'),
        ),
    ]