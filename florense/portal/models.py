from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Environment(models.Model):
    class Meta:
        db_table = "tbl_environment"

    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class Order(models.Model):
    class Meta:
        db_table = "tbl_order"

    id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    salesmen = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                 related_name='order_salesmen', null=True)
    inspector = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  related_name='order_inspector', null=True)
    environment = models.ForeignKey(Environment, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id


class Product(models.Model):
    class Meta:
        db_table = "tbl_product"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    allocations = models.ManyToManyField(Order, through='Allocation')

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Allocation(models.Model):
    class Meta:
        db_table = "tbl_allocation"

    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    path_image = models.TextField(blank=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Allocation, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id

