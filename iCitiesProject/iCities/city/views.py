from django.shortcuts import render
from .models import *
from django.utils.timezone import now

import csv, io, json
import os.path
import pandas as pd, numpy as np


# Create your views here.

def listCities(request, typeList=0):
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
    if typeList in range(1, 8):
        cities = City.objects.filter(typeCity__id=typeList)
    elif typeList is 0:
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
    city = City.objects.get(id=city_id)
    indic = ListIndicators.objects.filter(city=city)
    total = 0
    perfTotal = 0
    for i in indic:
        total += i.valueDec
        perfTotal += 1
    perfTotal *= 10
    print("Cities -", city.name)
    print(request.path)
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'viewCity.html',
        context={'city': city, "listInd": indic.order_by("indicator__num"), "total": total, "perfect": perfTotal},
    )


def compareCity(request, city1_id, city2_id):
    """
    Функция отображения сравнения городов.
    """
    city1 = City.objects.get(id=city1_id)
    city2 = City.objects.get(id=city2_id)

    print("Cities -", city1.name)
    print(request.path)
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'compareCity.html',
        context={'city1': city1, 'city2': city2, },
    )


def updateListCities(request):

    for city in City.objects.all():
        if ListIndicators.objects.filter(city=city, indicator__num=3).exists() is False:
            ListIndicators(city=city, indicator=Indicator.objects.get(num=3),
                           value=np.random.triangular(45, 55, 95)).save()

    list = ListIndicators.objects.all()

    
    for i in TypeCity.objects.all():
        toDecSystem(3, i.id)

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
        context={"lI": list.order_by("city__name"), },
    )

    pass


def deleteDupData(request):
    """
    for city in City.objects.values_list('name', flat=True).distinct():
        City.objects.filter(pk__in=City.objects.filter(name=city).values_list('id', flat=True)[1:]).delete()
    """
    l = ListIndicators.objects.all().delete()
    pass


def toDecSystem(ind, typeCity):
    for climate in ['C', 'D']:
        allList = ListIndicators.objects.filter(indicator__num=ind).filter(city__typeCity=typeCity).filter(city__climate=climate)
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
