# Generated by Django 4.2.1 on 2023-06-23 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApi', '0002_alter_product_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='Id'),
        ),
    ]
