from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('user/', views.UserEdit.as_view()),
    path('user/add', views.UserCreate.as_view()),
]
