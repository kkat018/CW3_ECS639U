# Generated by Django 4.1.3 on 2022-12-11 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionApp', '0003_remove_user_item_item_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_posted',
            field=models.DateField(auto_now=True, verbose_name='Date Posted'),
        ),
        migrations.AlterField(
            model_name='item',
            name='expiry_date',
            field=models.DateTimeField(verbose_name='Bid Expiry Date'),
        ),
    ]