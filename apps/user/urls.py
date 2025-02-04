from django.urls import path
from apps.user import views

urlpatterns = [
    path('register/',views.CreateOrUpdateUserApiView.as_view()),
    path('login/',views.LoginApiView.as_view()),
    path('logout/',views.LogoutApiView.as_view()),
    path('user-forgetpassword/',views.UserForgetPasswordApiView.as_view()),


]
