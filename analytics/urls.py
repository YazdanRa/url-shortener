from django.urls import path, include

from . import views

urlpatterns = [
    path('<str:short_path>/', include([
        path('', views.visit_record, name='visit_record'),
        path('analytics', views.analytics, name='analytics')
    ]))
]