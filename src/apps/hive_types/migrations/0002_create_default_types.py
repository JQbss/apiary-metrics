# Generated by Django 5.1.6 on 2025-04-16 19:11

from django.db import migrations

def create_default_types(apps, schema_editor):
    HiveType = apps.get_model('hive_types', 'HiveType')

    types = [
        'Langstroth',
        'Top Bar',
        'Warre',
        'Flow Hive',
        'Beehaus',
        'Long Langstroth',
        'Horizontal Top Bar',
        'Vertical Top Bar',
        'Wielkopolski',
        'Other'
    ]

    # Create default types if they don't exist
    for hiveType in types:
        HiveType.objects.get_or_create(name=hiveType)

def reverse_create_default_types(apps, schema_editor):
    HiveType = apps.get_model('hive_types', 'HiveType')

    # Delete all types created by this migration
    HiveType.objects.filter(name__in=[
        'Langstroth',
        'Top Bar',
        'Warre',
        'Flow Hive',
        'Beehaus',
        'Long Langstroth',
        'Horizontal Top Bar',
        'Vertical Top Bar',
        'Wielkopolski',
        'Other'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('hive_types', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_types, reverse_create_default_types),
    ]
