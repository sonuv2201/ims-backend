from django.db import models

class Book(models.Model):
    desc = models.CharField(max_length=100)
    not_show = models.IntegerField()

    class Meta:
        # managed = False  # Django will not create or manage the table
        db_table = "book"  # Optional: specify the actual table name


