from django.db import models

class Gradepoints(models.Model):
    Grade=models.CharField(primary_key=True,max_length=20)
    Points=models.IntegerField()
    Status=models.CharField(max_length=1)
    Presence=models.CharField(max_length=7)

class Branchcodes(models.Model):
    Branch=models.CharField(max_length=100)
    Code=models.CharField(primary_key=True,max_length=2)
    Abbrevation=models.CharField(max_length=10)