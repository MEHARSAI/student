from django.db import models

# Create your models here.
class Student(models.Model):
    Name = models.CharField(max_length=20, null=False, primary_key=True)
    Rollnumber = models.IntegerField(null=False, unique=True)
    Dateofbirth = models.DateField(null=False,auto_now=True)
    marks = models.IntegerField(default=50)
    grade = models.CharField(max_length=5,default='A')

    def __str__(self):
        return self.Name