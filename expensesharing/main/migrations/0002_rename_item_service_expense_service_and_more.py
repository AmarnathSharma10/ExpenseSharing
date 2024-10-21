# Generated by Django 5.0.7 on 2024-10-21 02:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='item_service',
            new_name='service',
        ),
        migrations.AddField(
            model_name='expense',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='participantexpense',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='expense',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='shared_expenses', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='split_method',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
