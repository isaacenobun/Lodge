# Generated by Django 5.0.6 on 2024-07-20 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LodgeApp', '0025_alter_guest_number_alter_subscriptions_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_number',
        ),
        migrations.AddField(
            model_name='room',
            name='room_tag',
            field=models.CharField(default='Room', max_length=50),
        ),
    ]