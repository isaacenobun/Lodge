# Generated by Django 5.0.6 on 2024-07-16 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LodgeApp', '0023_alter_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('payment_status', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LodgeApp.company')),
            ],
        ),
    ]