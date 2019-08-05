from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    section = models.CharField(max_length=10)
    year = models.CharField(max_length=10)
