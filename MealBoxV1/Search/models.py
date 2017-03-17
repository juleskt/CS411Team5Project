from django.db import models

# Create your models here.

class Search(models.Model):
  searchText = models.CharField(max_length=200)
