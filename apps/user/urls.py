from django.urls import path
from apps.user import views

urlpatterns = [
    path('register/',views.CreateOrUpdateUserApiView.as_view(),name='user-register'),
]
