# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('user_profile/', user_profile_form, name='user_profile_form'),
    path('user_profiles/', user_profile_list, name='user_profile_list'),
    path('profiles/delete/<int:user_id>/', user_profile_delete, name='user_profile_delete'),
    path('', user_profile_list, name='user_profile_list'),
    path('manage/<int:user_id>/', user_profile_manage, name='user_profile_manage'),
    path('manage/', user_profile_manage, name='user_profile_manage_create'),
    path('delete/', delete_user_profile, name='delete_user_profile'),
]

