# Generated by Django 3.2.9 on 2021-12-15 03:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0003_auto_20211208_2231'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BalanceChange',
            new_name='Transaction',
        ),
    ]
