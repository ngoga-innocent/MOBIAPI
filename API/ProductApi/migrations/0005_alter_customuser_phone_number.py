# Generated by Django 4.2.1 on 2023-07-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApi', '0004_customuser_first_name_customuser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=255),
        ),
    ]