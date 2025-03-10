# Generated by Django 5.1.6 on 2025-03-03 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orderpayment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('percent_off', models.PositiveIntegerField(help_text='Percentage off (e.g., 10 for 10%)')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('currency', models.CharField(choices=[('usd', 'USD - US Dollar'), ('eur', 'EUR - Euro')], default='usd', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('percentage', models.PositiveIntegerField(help_text='Tax percentage (e.g., 10 for 10%)')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orderpayment.discount')),
                ('items', models.ManyToManyField(to='orderpayment.item')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orderpayment.tax')),
            ],
        ),
    ]
