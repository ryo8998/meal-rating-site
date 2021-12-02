from django.db import models

# Create your models here.


class Meal(models.Model):
    class MealTime(models.IntegerChoices):
        Morning = 1
        Afternoon = 2
        Evening = 3
    # MEAL_TIMING =[(1,"Morning"),(2,"Afternoon"),(3,"Evening")]
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    imageUrl = models.CharField(max_length=255)
    countryOfOrigin = models.CharField(max_length=128)
    typicalMealTime = models.IntegerField(choices=MealTime.choices)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MealRating(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    dateOfRating = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Ratinng of " +  self.meal.name
    