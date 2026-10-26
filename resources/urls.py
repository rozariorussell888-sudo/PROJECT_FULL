from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('resources/', views.resources, name='resources'),
    path('resources/<int:id>/', views.resource_detail, name='resource_detail'),
    path('my-resources/', views.my_resources, name='my_resources'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:id>/edit/', views.edit_item, name='edit_item'),
    path('items/<int:id>/delete/', views.delete_item, name='delete_item'),
    path('about/', views.about, name='about'),
]
