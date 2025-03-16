# Generated by Django 5.1.6 on 2025-03-16 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('viewer', 'Viewer'), ('admin', 'Admin'), ('beekeeper', 'Beekeeper')], default='beekeeper', max_length=20),
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
