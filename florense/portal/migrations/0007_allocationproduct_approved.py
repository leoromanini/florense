# Generated by Django 2.2 on 2020-07-26 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocationproduct',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
