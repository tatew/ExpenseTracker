# Generated by Django 3.2.9 on 2022-04-05 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0013_method_iconclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='method',
            name='iconClass',
        ),
    ]
