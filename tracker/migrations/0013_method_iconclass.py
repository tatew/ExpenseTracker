# Generated by Django 3.2.9 on 2022-04-05 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0012_method_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='iconClass',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]