from django.db import models

# Create your models here.


class Search(models.Model):
    searchText = models.CharField(max_length=200)


class SearchModel(models.Model):
    search_id = models.IntegerField()
    search_term = models.CharField(max_length=255)
    data_response = models.TextField()
    page_num = models.IntegerField()
    date_cached = models.DateField()

    class Meta:
        db_table = 'searchCache_tbl'
