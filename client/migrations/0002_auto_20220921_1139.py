# Generated by Django 3.2.8 on 2022-09-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_price',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(null=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]