# Generated by Django 5.1.6 on 2025-04-17 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hives', '0002_hive_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hive',
            name='aggression',
            field=models.CharField(choices=[('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High')], default='MEDIUM', max_length=20),
        ),
        migrations.AddField(
            model_name='hive',
            name='strength',
            field=models.CharField(choices=[('VERY_WEAK', 'Very Weak'), ('WEAK', 'Weak'), ('MEDIUM', 'Medium'), ('STRONG', 'Strong'), ('VERY_STRONG', 'Very Strong')], default='MEDIUM', max_length=20),
        ),
    ]
