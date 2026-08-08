from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('ajax/load-cities/', views.get_cities, name='get_cities'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('active-email/<str:encoded_user_id>/<str:token>/', views.active_email, name='active_email'),
    path('mobile_login/', views.mobile_login, name='mobile_login'),
    path('varify_otp/', views.varify_otp, name='varify_otp'),
]
