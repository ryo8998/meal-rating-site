from typing import Container
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from .models import Meal, MealRating
from .forms import MealForm, MealRatingForm
import datetime
from django.db.models import Count, Max, Min, Avg

# Create your views here.

class IndexView(View):

    def get(self,request):
        context = self.get_context_data()
        return render(request,"mealRatings/index.html",context=context)

    def post(self,request):
        form = MealForm(data=request.POST)
        context = self.get_context_data()
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            context = self.get_context_data()
            return render(request,'mealRatings/index.html',context=context)
        else:
            return Http404("Error")

    def get_context_data(self):
        context = {}
        context["morning"] = Meal.objects.filter(typicalMealTime=1)[:3]
        context["afternoon"] = Meal.objects.filter(typicalMealTime=2)[:3]
        context["evening"] = Meal.objects.filter(typicalMealTime=3)[:3]
        ninety_days_ago = datetime.date.today() - datetime.timedelta(days=1000)
        # print(datetime.date.today())
        context["recently_added"] = Meal.objects.filter(dateAdded__gte=ninety_days_ago,dateAdded__lte=datetime.datetime.now()).order_by("-dateAdded")[:3]
        context["top_rated_foods"] = Meal.objects.annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating__rating')).filter(rating_avg__gte=4.0).order_by("-rating_avg")[:3]
        context["forms"] = MealForm()
        print(context)
        return context

    

       
class CategoryListView(ListView):
    template_name = "mealRatings/category_list.html"
    model = Meal
    context_object_name = "meals"

   
    def get_queryset(self):
        if self.kwargs["category"] == "morning":
            query_set = Meal.objects.filter(typicalMealTime=1).annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating__rating')) 
        elif self.kwargs["category"] == "afternoon":
            query_set = Meal.objects.filter(typicalMealTime=2).annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating__rating')) 
        elif self.kwargs["category"] == "evening":
            query_set = Meal.objects.filter(typicalMealTime=3).annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating__rating')) 
        elif self.kwargs["category"] == "recently_added":
            ninety_days_ago = datetime.date.today() - datetime.timedelta(days=1000)
            # query_set = Meal.objects.order_by("dateAdded").filter(dateAdded__range=(ninety_days_ago,datetime.date.today())).annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating__rating')) 
            query_set = Meal.objects.order_by("-dateAdded").filter(dateAdded__range=(ninety_days_ago,datetime.datetime.now())).annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating__rating')) 

        else:
            query_set = Meal.objects.annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating__rating')).filter(rating_avg__gte=4.0).order_by("-rating_avg") 
            print(query_set)

        if self.request.GET.get('sort'):
            param = self.request.GET.get('sort')
            if param == "rating":
                query_set = query_set.order_by("-rating_avg")
            elif param == "country":
                query_set = query_set.order_by("countryOfOrigin")
            else:
                query_set = query_set.order_by("dateAdded")
            
        return query_set


    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = self.kwargs["category"].replace('_',' ')
        context["category"] = self.kwargs["category"]
        return context


class MealDetailView(View):

    def get(self,request,pk):
        context = {}
        context["meal"] = Meal.objects.filter(pk=pk).annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating'))[0]
        context["form"] = MealRatingForm()
        return render(request,"mealRatings/meal_detail.html",context=context)

    def post(self,request,pk):
        form = MealRatingForm(request.POST)
        context = {}
        context["form"] = form
        if form.is_valid():
            meal = Meal.objects.get(pk=pk)
            rating = MealRating(meal=meal,rating=form.cleaned_data['rating'])
            rating.save()
            context["meal"] = Meal.objects.filter(pk=pk).annotate(rating_avg = Avg('mealrating__rating'),num_of_rating = Count('mealrating'))[0]
            return redirect(to="/")
        else:
            return Http404("Error")
