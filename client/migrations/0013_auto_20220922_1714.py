# Generated by Django 3.2.8 on 2022-09-22 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_auto_20220922_1251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='buyer',
            new_name='client',
        ),
        migrations.RenameField(
            model_name='orderproduct',
            old_name='buyer',
            new_name='client',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]