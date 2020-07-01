from django.urls import path
from .views import AllLook, LookDetail

urlpatterns = [
    path('cruise-2019-20', AllLook.as_view()),
    path('cruise-2019-20/<int:look_num>/', LookDetail.as_view()),
]
