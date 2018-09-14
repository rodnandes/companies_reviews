from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=100)


class Review(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    rating = models.FloatField()
    title = models.CharField(max_length=200)
    summary = models.TextField()
    ip_address = models.CharField(max_length=20)
    submission_date = models.DateField()
