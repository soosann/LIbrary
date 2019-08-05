from django.db import models
from category.models import Category

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    categories = models.ManyToManyField(Category)
    cover = models.TextField(max_length=100000, blank=True, null=True)
    author = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=25000, blank=True, null=True)
    available = models.IntegerField(default=0)

    def __str__(self):
        return self.title