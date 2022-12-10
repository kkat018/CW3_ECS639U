# Generated by Django 4.1.1 on 2022-12-10 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionApp', '0002_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='expiry_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='answerdetails',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='biddetails',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='questiondetails',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
