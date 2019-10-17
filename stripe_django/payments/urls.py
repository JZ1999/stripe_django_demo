from django.urls import path

from . import views

urlpatterns = [
    path('api/charge/', views.DemoCharge.as_view({'post': 'create'}), name='api-charge'),
    path('charge/', views.charge, name='charge'),
    path('', views.HomePageView.as_view(), name='home'),
]
