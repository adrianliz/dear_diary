# Generated by Django 3.1.4 on 2021-01-02 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0011_auto_20210102_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='moods/avatars/noimage.png', upload_to='moods/avatars/'),
        ),
    ]