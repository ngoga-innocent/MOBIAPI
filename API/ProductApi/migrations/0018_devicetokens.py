# Generated by Django 4.2.1 on 2023-08-31 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApi', '0017_customuser_device_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceToken', models.TextField()),
            ],
        ),
    ]
