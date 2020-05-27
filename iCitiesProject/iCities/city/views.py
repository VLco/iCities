from django.shortcuts import render
from .models import *
from django.utils.timezone import now
from django.db.models import Count, QuerySet
from .forms import *

import csv, io, json
import os.path
import pandas as pd, numpy as np


# Create your views here.

def listCities(request, typeCity=0):
    """
    Функция отображения каталога городов.
    ////////////////////////////////////
    typeList =
    0 - default list
    1 - крупнейшие города с численностью населения от 1 млн. человек;
    2 - крупные города с численностью населения от 250 тыс. до 1 млн. человек;
    3 - большие города с численностью населения от 100 тыс. до 250 тыс. человек;
    4 - средние города с численностью населения от 50 тыс. до 100 тыс. человек;
    5 - малые города с численностью населения от 25 тыс. до 50 тыс. человек;
    6 - малые города с численностью населения от 5 тыс. до 25 тыс. человек;
    7 - малые города с численностью населения до 5 тыс. человек
    """
    num_cities = City.objects.all().count()
    cities = None
    if typeCity in range(1, 8):
        cities = City.objects.filter(typeCity__id=typeCity)
    elif typeCity is 0:
        cities = City.objects.all()
    cities = cities.order_by("name")
    listC = dict()
    for city in cities:
        letter = city.name[0]
        if letter in listC:
            listC[letter].append(city)
        else:
            listC[letter] = []
            listC[letter].append(city)

    print(request.path)
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'listCities.html',
        context={'num_cities': num_cities, 'cities_list': listC.items(), },
    )


def viewCity(request, city_id):
    """
    Функция отображения страниц городов.
    """
    print(city_id)
    category = CategoryIdicators.objects.all()
    city = City.objects.get(id=city_id)
    indicators = ListIndicators.getListbyCategories(city)
    total = 0
    totalCategory = {}
    perfTotal = 0
    perfTotalCategory = {}
    for c in category:
        totalCategory[c.name] = 0
        perfTotalCategory[c.name] = 0
        if indicators.get(c.name) is not None:
            for i in indicators[c.name]:
                totalCategory[c.name] += i.valueDec
                perfTotalCategory[c.name] += 1
            perfTotal += perfTotalCategory[c.name]
            total += totalCategory[c.name]
            perfTotalCategory[c.name] *= 10
    perfTotal *= 10
    print("Cities -", city.name)
    print(request.path)
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'viewCity.html',
        context={'city': city, "listInd": indicators, "total": total, "totalCategory": totalCategory,
                 "perfect": perfTotal, "perfectCategory": perfTotalCategory},
    )


def ratingList(request):
    """
    Функция отображения рейтинга
    """
    types = ListFilter.typeCities(request.POST or None)
    clim = ListFilter.climate(request.POST or None, initial={'climate': 'ALL'})
    climate = 0
    typeCity = 0
    if request.method == "POST" and types.is_valid() and clim.is_valid():
        typeCity = list()
        print(request.POST)
        if 'ALL' not in request.POST.get('climate'):
            climate = request.POST.get('climate')

        if request.POST.get('all', False):
            typeCity.append(0)
        if request.POST.get('t1', False):
            typeCity.append(1)
        if request.POST.get('t2', False):
            typeCity.append(2)
        if request.POST.get('t3', False):
            typeCity.append(3)
        if request.POST.get('t4', False):
            typeCity.append(4)
        if request.POST.get('t5', False):
            typeCity.append(5)
        if request.POST.get('t6', False):
            typeCity.append(6)
        if request.POST.get('t7', False):
            typeCity.append(7)
    if typeCity is not 0 and climate is not 0:
        cities = City.objects.filter(typeCity__id__in=typeCity, climate__in=climate)
    elif typeCity is not 0:
        cities = City.objects.filter(typeCity__id__in=typeCity)
    elif climate is not 0:
        cities = City.objects.filter(climate__in=climate)
    else:
        cities = City.objects.all()
    d = dict()

    for city in cities:
        total = 0
        for ind in ListIndicators.objects.filter(city=city):
            total += ind.getValDec()
        d[city] = total
    tmp = list(d.items())
    tmp.sort(key=lambda i: i[1])
    tmp.reverse()
    li = dict(tmp)
    print(li)
    return render(
        request=request,
        template_name='ratingCities.html',
        context={"list": li, 'clim': clim, 'types': types, },
    )
    pass


def compareCity(request, city1_id, city2_id):
    """
    Функция отображения сравнения городов.
    """
    cities = []
    cities.append(City.objects.get(id=city1_id))
    cities.append(City.objects.get(id=city2_id))
    print(request.path)
    category = CategoryIdicators.objects.all()
    indicators = []
    total = {}
    perfTotal = 0
    perfTotalCategory = {}
    tmp = []
    for city in cities:
        total[city.id] = 0
        totalCategory = {}
        for c in category:
            indicators.append(ListIndicators.getListbyCategories(city))
            totalCategory[c.name] = 0
            perfTotalCategory[c.name] = 0
            if indicators[len(indicators) - 1].get(c.name) is not None:
                for i in indicators[len(indicators) - 1][c.name]:
                    totalCategory[c.name] += i.getValDec()
                    perfTotalCategory[c.name] += 1
                perfTotal += perfTotalCategory[c.name]
                total[city.id] += totalCategory[c.name]
                perfTotalCategory[c.name] *= 10
        tmp.append(totalCategory)
    indicators, sumval = ListIndicators.getListforCompare(city1_id, city2_id)
    perfTotal *= 5
    total = [total[cities[0].id], total[cities[1].id]]
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'compareCity.html',
        context={'cities': cities, "listInd": indicators, "total": total, "totalCategory": tmp,
                 "perfect": perfTotal, "perfectCategory": perfTotalCategory, "sumVal": sumval, },
    )


def updateListCities(request):
    num = 36
    for city in City.objects.all():
        if ListIndicators.objects.filter(city=city, indicator__num=num).exists() is False:
            ListIndicators(city=city, indicator=Indicator.objects.get(num=num),
                           value=np.random.triangular(30, 60, 90)).save()

    list = ListIndicators.objects.filter(indicator__num=num)

    for i in TypeCity.objects.all():
        toDecSystem(num, i.id)

    list = ListIndicators.objects.values('indicator__num', 'indicator__name').annotate(Count('indicator')).order_by(
        'indicator__num')

    """ 
    
    path = os.path.join(os.path.dirname(__file__), 'static', 'city.csv')
    pathj = os.path.join(os.path.dirname(__file__), 'static', 'city.csv-metadata.json')

    csv_file = csv.reader(io.open(path, "r", encoding='utf-8'), delimiter=",")
    csv_file = list(csv_file)
    json_file = json.load(io.open(pathj, "r", encoding='utf-8'))
    for row in csv_file:
        if row is csv_file[0] or row[9] is None:
            continue
        if row[22] is not int:
            pop = list(row[22])
            tmp = []
            for i in pop:
                try:
                    int(i)
                    tmp += i
                except ValueError:
                    break
            row[22] = int("".join(str(i) for i in tmp))
        if Region.objects.filter(name=row[5]).exists() is False:
            Region(name=row[5], type=row[4]).save()
        if City.objects.filter(name=row[9], population=row[22],
                               region=Region.objects.get(name=row[5], type=row[4])).exists() is False:
            City(name=row[9], population=row[22], region=Region.objects.get(name=row[5], type=row[4])).save()
    """
    return render(
        request,
        'updListCities.html',
        context={"lI": list, },
    )

    pass


def deleteDupData(request):
    """
    for city in City.objects.values_list('name', flat=True).distinct():
        City.objects.filter(pk__in=City.objects.filter(name=city).values_list('id', flat=True)[1:]).delete()
    """
    # l = ListIndicators.objects.filter(indicator__num=8).delete()
    pass


def toDecSystem(ind, typeCity):
    for climate in ['C', 'D']:
        allList = ListIndicators.objects.filter(indicator__num=ind).filter(city__typeCity=typeCity).filter(
            city__climate=climate)
        data = []
        for i in list(allList.values_list("value")):
            data.append(i[0])
        quantiles = pd.DataFrame(np.array(data)).quantile([0.25, 0.5, 0.75])[0].to_list()
        print(quantiles)
        Min = quantiles[0] - 0.5 * (quantiles[2] - quantiles[0])
        Max = quantiles[2] + 0.5 * (quantiles[2] - quantiles[0])
        x = []
        for i in range(1, 10, 1):
            x.append(Min + (i * (Max - Min) / 9))
        print(Max, Min)
        print(x)
        test = []
        h = x[1] - x[0]
        for i in allList:
            j = 1
            if i.date < now():
                while True:
                    if i.value >= Min + h * j:
                        j = j + 1
                    elif i.value >= Max:
                        i.valueDec = 10
                        break
                    elif i.value < Min + h * j:
                        i.valueDec = j if j <= 10 else 10
                        break
                    else:
                        print("Error to dec")
                        i.valueDec = 0
                        break
                if ind in [1, 4, 7, 9, 30, 31]:
                    i.valueDec = 11 - i.valueDec
                i.date = now()
                i.save()
            test.append(i.valueDec)

    print(allList.count())
    return test
    pass
