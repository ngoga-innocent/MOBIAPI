# Generated by Django 4.2.1 on 2023-06-21 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_name', to='ProductApi.shop'),
        ),
    ]
