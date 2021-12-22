from rest_framework import serializers
from .models import Car, Cars_rating
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'make', 'model')

class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars_rating
        fields = ('id', 'car_id', 'rating')