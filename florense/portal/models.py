from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils import timezone


class Environment(models.Model):
    class Meta:
        db_table = "tbl_environment"

    name = models.CharField(max_length=150)
    active = models.BooleanField(default=True)

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
    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id


class Label(models.Model):
    class Meta:
        db_table = "tbl_label"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Label, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    class Meta:
        db_table = "tbl_product"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Room(models.Model):
    class Meta:
        db_table = "tbl_room"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    allocations = models.ManyToManyField(Product, through='Allocation')
    labels = models.ManyToManyField(Label, through='RoomLabel')
    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Room, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class ProductBelongs(models.Model):
    class Meta:
        db_table = "tbl_product_belongs"

    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(ProductBelongs, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id


class LabelBelongs(models.Model):
    class Meta:
        db_table = "tbl_label_belongs"

    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(LabelBelongs, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id


class Allocation(models.Model):
    class Meta:
        db_table = "tbl_allocation"

    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_belong = models.ForeignKey(ProductBelongs, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

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


class RoomLabel(models.Model):
    class Meta:
        db_table = "tbl_room_label"

    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    label_belong = models.ForeignKey(LabelBelongs, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    content = models.TextField(blank=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(RoomLabel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id
