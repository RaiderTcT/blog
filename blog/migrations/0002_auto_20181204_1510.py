# Generated by Django 2.1.3 on 2018-12-04 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='collection',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='blog',
            name='text',
            field=mdeditor.fields.MDTextField(blank=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='collection',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collect_blog', to='blog.Blog'),
        ),
        migrations.AddField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collect_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
