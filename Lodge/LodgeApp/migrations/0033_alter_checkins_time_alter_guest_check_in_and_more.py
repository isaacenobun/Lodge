# Generated by Django 5.0.6 on 2024-07-28 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LodgeApp', '0032_alter_guest_revenue_alter_guest_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkins',
            name='time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='guest',
            name='check_in',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
