from djongo import models

class Car(models.Model):
    make = models.TextField()
    model = models.TextField()
    def __str__(self):
        return self.model

class Cars_rating(models.Model):
    car_id = models.IntegerField()
    rating = models.IntegerField()
    def __int__(self):
        return self.car_id
