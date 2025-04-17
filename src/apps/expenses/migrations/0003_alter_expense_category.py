# Generated by Django 5.1.6 on 2025-04-16 17:13

import apps.expenses.models
from django.db import migrations

from utils.fields import LowerCaseField


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=LowerCaseField(max_length=255),
        ),
    ]
