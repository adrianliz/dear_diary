# Generated by Django 3.1.4 on 2021-01-15 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0012_auto_20210102_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatars/noimage.png', upload_to='avatars/'),
        ),
    ]