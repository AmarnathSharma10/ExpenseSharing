# Generated by Django 5.0.7 on 2024-10-20 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_service', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=3, max_digits=10)),
                ('split_method', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_expenses', to='accounts.profile')),
                ('participants', models.ManyToManyField(related_name='shared_expenses', to='accounts.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_owed', models.DecimalField(decimal_places=3, max_digits=10)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.expense')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
    ]