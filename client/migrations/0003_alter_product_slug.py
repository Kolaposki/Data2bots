# Generated by Django 3.2.8 on 2022-09-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20220921_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', editable=False),
        ),
    ]
