from django.shortcuts import render
from city.models import *

# Create your views here.
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_cities = City.objects.all().count()
    print("Home")
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_cities': num_cities},
    )
