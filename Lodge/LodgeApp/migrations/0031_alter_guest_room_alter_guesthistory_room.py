# Generated by Django 5.0.6 on 2024-07-25 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LodgeApp', '0030_alter_guest_room_alter_guesthistory_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LodgeApp.room'),
        ),
        migrations.AlterField(
            model_name='guesthistory',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LodgeApp.room'),
        ),
    ]
