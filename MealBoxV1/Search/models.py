from django.db import models

# Create your models here.


class Search(models.Model):
    searchText = models.CharField(max_length=200)


class SearchModel(models.Model):
    searchID = models.IntegerField()
    searchTerm = models.CharField()
    dataResponse = models.TextField()
    pageNum = models.IntegerField()
    dateCached = models.DateField()