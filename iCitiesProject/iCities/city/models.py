from django.db import models


# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=100, default='',)
    def __str__(self):
        return self.name


class City(models.Model):
    id = models.AutoField(primary_key=True)

    CLIMATE_CHOICES = [
        ('D', 'Discomfort'),
        ('C', 'Comfort'),
    ]

    name = models.CharField(max_length=50, help_text="City name", null=False)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    population = models.IntegerField()
    climate = models.CharField(
        max_length=2,
        choices=CLIMATE_CHOICES,
        default='C',
    )

    #objects = models.Manager()

    def __str__(self):
        return self.name



class Indicator(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.name


class ListIndicators(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    value = models.FloatField()
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)

    def __str__(self):
        return self.indicator.name + "_" + self.city.name

    def getVal(self):
        return self.value
