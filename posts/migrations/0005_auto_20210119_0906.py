# Generated by Django 3.1.4 on 2021-01-19 03:06

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='overview',
            field=tinymce.models.HTMLField(),
        ),
    ]