from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('user/', views.UserEdit.as_view()),
    path('manage-slot/', views.Slots.as_view()),
    path('slot-requests/', views.SlotReqeusts.as_view()),
]
