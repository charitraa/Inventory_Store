# Generated by Django 5.0.1 on 2024-01-17 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['user__first_name', 'user__last_name'], 'permissions': [('view_history', 'Can view history')]},
        ),
    ]
