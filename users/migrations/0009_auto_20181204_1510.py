# Generated by Django 2.1.3 on 2018-12-04 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20181129_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default.jpg', null=True, upload_to='avatar/%Y/%m/%d', verbose_name='avatar'),
        ),
    ]
