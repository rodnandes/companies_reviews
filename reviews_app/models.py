from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Company(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'companies'


class Review(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(0.5)])
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    ip_address = models.GenericIPAddressField()
    submission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
