from django.urls import path
from . import views

urlpatterns = [
        path("", views.user_login, name="home"),
        path("login", views.user_login, name="login"),
        path("logout", views.user_logout, name="logout"),
        path("register", views.user_create, name="register"),
        path('retrieve_record/<int:pk>', views.record_retrieve, name='record_retrieve'),
        path('delete_record/<int:pk>', views.record_delete, name='record_delete'),
        path('create_record', views.record_create, name='record_create'),
        path('update_record/<int:pk>', views.record_update, name='record_update'),
]
