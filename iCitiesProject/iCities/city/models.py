from django.db import models
from django.utils.timezone import now


# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=100, default='', )

    def __str__(self):
        return self.name


class TypeCity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class CategoryIdicators(models.Model):
    name = models.CharField(max_length=100)

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
    typeCity = models.ForeignKey(TypeCity, on_delete=models.SET_NULL, null=True)
    climate = models.CharField(
        max_length=2,
        choices=CLIMATE_CHOICES,
        default='C',
    )

    # objects = models.Manager()

    def __str__(self):
        return self.name


class Indicator(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=250)
    desc = models.TextField()
    formuls = models.CharField(max_length=50)
    param = models.TextField()
    category = models.ForeignKey(CategoryIdicators, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.num) + "-" + self.name

    def getParam(self):
        return self.param.split(";")


class ListIndicators(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    value = models.FloatField()
    valueDec = models.IntegerField(default=0)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    param = models.TextField(null=True, default="-")
    date = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.indicator.__str__() + " " + self.city.name

    def getVal(self):
        return self.value

    def getValDec(self):
        return self.valueDec

    def getListbyCategories(city):
        list = {}
        categories = CategoryIdicators.objects.all()
        for category in categories:
            if ListIndicators.objects.filter(indicator__category=category, city=city).order_by(
                    "indicator__num").exists():
                list[category.name] = ListIndicators.objects.filter(indicator__category=category, city=city).order_by(
                    "indicator__num")
        return list

    def getListforCompare(city1, city2):
        list = {}
        sumVal = {}
        cities = City.objects.filter(id__in=[city1, city2])
        print(cities)
        categories = CategoryIdicators.objects.all()
        indicators = Indicator.objects.all()
        for category in categories:
            listbyIndicators = {}
            sumValbyIndicators = {}
            for indicator in indicators.filter(category=category):
                listbyCities = {}
                for city in cities:
                    if ListIndicators.objects.filter(city=city, indicator=indicator).exists():
                        listbyCities[city.name] = ListIndicators.objects.filter(city=city, indicator=indicator).order_by("indicator__num")
                if listbyCities.__len__() != 0:
                    listbyIndicators[indicator.name] = listbyCities
                    sumValbyIndicators[indicator.name] = 0
                    for i in listbyIndicators[indicator.name].values():
                        sumValbyIndicators[indicator.name] += i[0].getValDec()
            if listbyIndicators.__len__() != 0:
                    list[category.name] = listbyIndicators
                    sumVal[category.name] = sumValbyIndicators
        return list, sumVal
