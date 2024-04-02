from django.db import models

class Chair(models.Model):
    model = models.CharField(max_length=100)
    designer = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    release = models.IntegerField()

    def __str__(self):
        return self.model
