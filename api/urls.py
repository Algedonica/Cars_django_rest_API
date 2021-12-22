from django.urls import path

from api import views
urlpatterns = [
    path('api/cars', views.cars_list),
    path('api/cars/<int:pk>', views.cars_list_delete),
    path('api/rate', views.rates_list),
    path('api/popular', views.popular_list),
]