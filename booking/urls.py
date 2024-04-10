from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('user/', views.UserEdit.as_view(), name='user-edit'),
    path('manage-slot/', views.Slots.as_view(), name = 'manage-slot'),
    path('slot-requests/', views.SlotReqeusts.as_view(), name = 'slot-requests'),
]
