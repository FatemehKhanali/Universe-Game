from importlib.util import module_for_loader
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models import Q

from accounts.models import city





class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class BaseModel(models.Model):
    deleted = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = BaseModelManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()


class Category(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Game(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.IntegerField()
    image = models.ImageField()
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Cart(BaseModel):
    quantity = models.PositiveIntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Order(BaseModel):
    total_price = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(null=True)
    note = models.CharField(max_length=200, blank=True)
    diffrent_address = models.BooleanField(default=False, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    address = models.CharField(max_length=500)
    city = models.ForeignKey(city, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=11)



class OrderGame(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()


class PaymentLog(models.Model):
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.PositiveIntegerField()
    order_id = models.PositiveIntegerField()
    status = models.CharField(max_length=100)
    error_code = models.CharField(max_length=200)


