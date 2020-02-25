from django.shortcuts import render
from .models import *
import csv, io, json
import os.path


# Create your views here.

def list_cities(request):
    """
    Функция отображения каталога городов.
    """
    # Генерация "количеств" некоторых главных объектов
    num_cities = City.objects.all().count()
    cities = City.objects.all().order_by('name')
    print("Cities -", num_cities)
    print(request.path)
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'listCities.html',
        context={'num_cities': num_cities, 'cities_list': cities, },
    )


def viewCity(request, city_id):
    """
    Функция отображения страниц городов.
    """
    print(city_id)
    city = City.objects.get(id=city_id)
    print("Cities -", city.name)
    print(request.path)
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'viewCity.html',
        context={'city': city, },
    )

def compareCity(request, city1_id, city2_id):
    """
    Функция отображения страниц городов.
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
        if City.objects.filter(name=row[9], population=row[22], region=Region.objects.get(name=row[5], type=row[4])).exists() is False:
            City(name=row[9], population=row[22], region=Region.objects.get(name=row[5], type=row[4])).save()
    return render(
        request,
        'updListCities.html',
        context={'list': csv_file[1], 'listj': list(json_file["tableSchema"]["columns"]),},
    )
    pass


def deleteDupData(request):
    for city in City.objects.values_list('name', flat=True).distinct():
        City.objects.filter(pk__in=City.objects.filter(name=city).values_list('id', flat=True)[1:]).delete()
    pass