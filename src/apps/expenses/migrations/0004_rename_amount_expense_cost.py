# Generated by Django 5.1.6 on 2025-04-16 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_alter_expense_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='amount',
            new_name='cost',
        ),
    ]
