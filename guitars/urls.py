from django.urls import path, re_path
from . import views

# URL mapování - seznam URL adres pro aplikaci guitars
urlpatterns = [
    path('', views.index, name='index'),
    path('guitars/', views.GuitarListView.as_view(), name='guitars'),
    path('guitars/types/<str:type_name>/', views.GuitarListView.as_view(), name='guitar-type'),
    path('guitars/<int:pk>/', views.GuitarDetailView.as_view(), name='guitar-detail'),
    path('guitar/create/', views.GuitarCreate.as_view(), name='guitar-create'),
    path('guitars/<int:pk>/update/', views.GuitarUpdate.as_view(), name='guitar-update'),
    path('guitars/<int:pk>/delete/', views.GuitarDelete.as_view(), name='guitar-delete'),
    path('clear_cache/', views.clear_cache),
]

