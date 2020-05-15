from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', include([
        path('', views.dashboard, name='dashboard'),
        path('create/', views.create, name='create'),
    ])),
]
