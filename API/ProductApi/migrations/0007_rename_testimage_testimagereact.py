# Generated by Django 4.2.1 on 2023-05-16 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApi', '0006_alter_testimage_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestImage',
            new_name='TestImageReact',
        ),
    ]