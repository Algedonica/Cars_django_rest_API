from json.encoder import JSONEncoder
from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 

from api.models import Car, Cars_rating
from api.serializers import CarSerializer, CarRatingSerializer

from statistics import mean

#Car existance check
import requests
def car_checker(x):
    link='https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/'+x['make']+'?format=json'
    request=requests.get(link).json()
    models=request['Results']
    models_arr=[]
    for i in models:
        models_arr.append(i['Model_Name'])
    if x['model'] in models_arr:
        
        return True
    else:
        return False

#Cars
@api_view(['GET', 'POST'])
def cars_list(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        cars_serializer = CarSerializer(cars, many=True)

        for x in cars_serializer.data:
            rates = Cars_rating.objects.filter(car_id__exact=x['id']) 
            if rates.exists():
                rates_arr=[]
                for item in rates:
                    rates_arr.append(item.rating)
                avg = mean(rates_arr)
                x['avg_rating'] = round(avg,1)
            else:
                x['avg_rating'] = 0
        return JsonResponse(cars_serializer.data, safe=False)

    elif request.method == 'POST':
        cars_data = JSONParser().parse(request)
        cars_serializer = CarSerializer(data=cars_data)
        
        if cars_serializer.is_valid():
            if car_checker(cars_serializer.validated_data)==True:
                try:
                    cars_serializer.save()
                    return JsonResponse(cars_serializer.data, status=status.HTTP_201_CREATED)
                except:
                    return JsonResponse(cars_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
        return JsonResponse(cars_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def cars_list_delete(request, pk):
    
    try: 
        car = Car.objects.get(pk=pk) 
    except Car.DoesNotExist: 
        return JsonResponse( status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE': 
        car.delete() 
        return JsonResponse( status=status.HTTP_204_NO_CONTENT) 

#Rates
@api_view(['POST'])
def rates_list(request):
    rates_data = JSONParser().parse(request)

    try: 
        Car.objects.get(pk=rates_data['car_id']) 
    except Car.DoesNotExist: 
        return JsonResponse( status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        rates_serializer = CarRatingSerializer(data=rates_data)
        if rates_serializer.is_valid():
            try:
                rates_serializer.save()
                return JsonResponse(rates_serializer.data, status=status.HTTP_201_CREATED)
            except:
                return JsonResponse(rates_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Popular
@api_view(['GET'])
def popular_list(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        cars_serializer = CarSerializer(cars, many=True)

        for x in cars_serializer.data:
            rates = Cars_rating.objects.filter(car_id__exact=x['id']) 
            if rates.exists():
                x['rates_number'] = len(rates)
            else:
                x['rates_number'] = 0
        total=sorted(cars_serializer.data, key=lambda rate: rate['rates_number'], reverse=True) 
        return JsonResponse(total, safe=False)