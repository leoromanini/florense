from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils import timezone


class Environment(models.Model):
    class Meta:
        db_table = "tbl_environment"

    name = models.CharField(max_length=150)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
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

    def __str__(self):
        return self.name


class Room(models.Model):
    class Meta:
        db_table = "tbl_room"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    products = models.ManyToManyField(Product, through='ProductPermission')
    labels = models.ManyToManyField(Label, through='LabelPermission')
    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Room, self).save(*args, **kwargs)

    def __str__(self):
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
    rooms = models.ManyToManyField(Room, through='AllocationRoom')
    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class ProductPermission(models.Model):
    class Meta:
        db_table = "tbl_product_permission"

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
        return super(ProductPermission, self).save(*args, **kwargs)

    def __str__(self):
        return str('{} <- {}'.format(self.room.name, self.product.name))


class LabelPermission(models.Model):
    class Meta:
        db_table = "tbl_label_permission"

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
        return super(LabelPermission, self).save(*args, **kwargs)

    def __str__(self):
        return str('{} <- {}'.format(self.room.name, self.label.name))


class AllocationRoom(models.Model):
    class Meta:
        db_table = "tbl_allocation_room"

    id = models.AutoField(primary_key=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AllocationRoom, self).save(*args, **kwargs)

    def __str__(self):
        return str('{} <- {}'.format(self.order.id, self.room.name))


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'order_files/{}/{}'.format(instance.allocation_room.order.id,
                                      instance.allocation_room.room.name,
                                      filename)


class AllocationProduct(models.Model):
    class Meta:
        db_table = "tbl_allocation_product"

    id = models.AutoField(primary_key=True)
    product_permission = models.ForeignKey(ProductPermission, on_delete=models.CASCADE)
    allocation_room = models.ForeignKey(AllocationRoom, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    image = models.ImageField(blank=True, upload_to=user_directory_path)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AllocationProduct, self).save(*args, **kwargs)

    def __str__(self):
        return str('{} <- {}'.format(self.product_permission.room.name, self.product_permission.product.name))


class AllocationLabel(models.Model):
    class Meta:
        db_table = "tbl_allocation_label"

    id = models.AutoField(primary_key=True)
    label_permission = models.ForeignKey(LabelPermission, on_delete=models.CASCADE)
    allocation_room = models.ForeignKey(AllocationRoom, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    content = models.TextField(blank=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AllocationLabel, self).save(*args, **kwargs)

    def __str__(self):
        return str('{} <- {}'.format(self.label_permission.room.name, self.label_permission.label.name))
