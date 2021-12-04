# Generated by Django 3.2.9 on 2021-12-04 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('vendor', models.CharField(max_length=200)),
                ('reason', models.CharField(max_length=500)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
