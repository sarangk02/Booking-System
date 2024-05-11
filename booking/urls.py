from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # Home page
    path('user/', views.UserEdit.as_view(), name='user-edit'),  # User edit page
    path('manage-slot/', views.Slots.as_view(), name='manage-slot'),  # Manage slots page
    path('slot-requests/', views.SlotReqeusts.as_view(), name='slot-requests'),  # Slot requests page
    path('verify/email/', views.VerifyEmail.as_view(), name='verify-email'),  # Verify email page
]
