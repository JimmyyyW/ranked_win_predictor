# Generated by Django 2.2.1 on 2019-05-23 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_auto_20190523_1900'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predict',
            old_name='username',
            new_name='user',
        ),
    ]
