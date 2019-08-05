from django.db import models
from books.models import Book
from students.models import Student

# Create your models here.
class Borrow(models.Model):
    book = models.ManyToManyField(Book)
    student = models.ManyToManyField(Student)
    qty = models.IntegerField(default=0)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=25)