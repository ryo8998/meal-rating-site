from django.urls import path
from .views import IndexView, CategoryListView, MealDetailView,LoginView

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path("list/<str:category>", CategoryListView.as_view(),name="category_list"),
    path("detail/<int:pk>", MealDetailView.as_view(),name="meal_detail"),
    path("login", LoginView.as_view(), name="login")
]
