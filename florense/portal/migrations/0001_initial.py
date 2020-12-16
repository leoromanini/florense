# Generated by Django 2.2 on 2020-07-09 01:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tbl_environment',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_label',
            },
        ),
        migrations.CreateModel(
            name='LabelPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Label')),
            ],
            options={
                'db_table': 'tbl_label_permission',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('environment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='portal.Environment')),
                ('inspector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_inspector', to=settings.AUTH_USER_MODEL)),
                ('salesmen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_salesmen', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_product',
            },
        ),
        migrations.CreateModel(
            name='ProductPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Product')),
            ],
            options={
                'db_table': 'tbl_product_permission',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('labels', models.ManyToManyField(through='portal.LabelPermission', to='portal.Label')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Order')),
                ('products', models.ManyToManyField(through='portal.ProductPermission', to='portal.Product')),
            ],
            options={
                'db_table': 'tbl_room',
            },
        ),
        migrations.AddField(
            model_name='productpermission',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Room'),
        ),
        migrations.AddField(
            model_name='labelpermission',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Room'),
        ),
        migrations.CreateModel(
            name='AllocationProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('path_image', models.TextField(blank=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('product_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.ProductPermission')),
            ],
            options={
                'db_table': 'tbl_allocation_product',
            },
        ),
        migrations.CreateModel(
            name='AllocationLabel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('content', models.TextField(blank=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('label_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.LabelPermission')),
            ],
            options={
                'db_table': 'tbl_allocation_label',
            },
        ),
    ]
