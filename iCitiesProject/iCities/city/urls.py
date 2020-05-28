from django.urls import path
from . import views

urlpatterns = [
    path('list', views.listCities, name="listCities"),
    path('list<int:typeCity>', views.listCities, name="listCities"),
    path('<int:city_id>', views.viewCity, name="viewCity"),
    path('<int:city1_id>vs<int:city2_id>', views.compareCity, name="compareCity"),
    path('upd', views.updateListCities, name="updList"),
    path('dnvd', views.deleteDupData, ),
    path('rating', views.ratingList, name="rating")
]
