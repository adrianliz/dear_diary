# Generated by Django 3.1.4 on 2021-01-28 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0017_profile_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
    ]
