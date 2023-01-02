from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.name