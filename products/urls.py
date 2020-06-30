from django.urls import path
from .views import BagView, DetailView, FilterView

urlpatterns = [
                path('/chanel-19', BagView.as_view()),
                path('/chanel-19/detail/<int:bag_num>', DetailView.as_view()),
                path('/chanel-19/filter', FilterView.as_view()),
              ]
