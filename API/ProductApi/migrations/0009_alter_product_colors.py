# Generated by Django 4.2.1 on 2023-05-16 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApi', '0008_test_delete_testimagereact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='colors',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='color', to='ProductApi.color'),
        ),
    ]