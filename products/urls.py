from django.urls import path
from .views import (
    BagView,
    BagDetail,
    AllLook,
    LookDetail
)

urlpatterns = [
    path('/cruise-2019-20', AllLook.as_view()),
    path('/cruise-2019-20/<int:look_num>', LookDetail.as_view()),
    path('/chanel-19', BagView.as_view()),
    path('/chanel-19/detail/<slug:query_bag_code>', BagDetail.as_view()),
]
