from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_cities, name = "listCities"),
    path('<int:city_id>', views.viewCity, name = "viewCity"),
    path('<int:city1_id>vs<int:city2_id>', views.compareCity, name = "compareCity"),
    path('upd', views.updateListCities, name = "updList"),
    path('dnvd', views.deleteDupData, ),

]