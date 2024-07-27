# Generated by Django 5.0.6 on 2024-06-09 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LodgeApp', '0008_checkins'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('regular', 'Regular'), ('business', 'Business'), ('executive', 'Executive')], default='Regular', max_length=50),
        ),
    ]