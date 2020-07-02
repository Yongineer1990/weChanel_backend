from django.urls import path
from .views import BagView, DetailView

urlpatterns = [
    path('/chanel-19', BagView.as_view()),
    path('/chanel-19/detail/<slug:query_bag_code>', DetailView.as_view()),
]
