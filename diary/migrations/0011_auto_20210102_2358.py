# Generated by Django 3.1.4 on 2021-01-02 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0010_auto_20210102_2358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='address1',
            new_name='address',
        ),
    ]