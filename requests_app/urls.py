from django.urls import path
from . import views
urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:id>/open/', views.open_notification, name='open_notification'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('requests/create/', views.create_request, name='create_request'),
    path('resources/<int:id>/send-request/', views.send_product_request, name='send_product_request'),
    path('requests/', views.received_requests, name='received_requests'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('requests/<int:id>/accept/', views.accept_product_request, name='accept_product_request'),
    path('requests/<int:id>/reject/', views.reject_product_request, name='reject_product_request'),
    path('my-requests/<int:id>/cancel/', views.cancel_product_request, name='cancel_product_request'),
    path('resource-requests/<int:id>/respond/', views.respond_to_resource_request, name='respond_to_resource_request'),
    path('resource-requests/', views.resource_request_list, name='resource_request_list'),
    path('resource-requests/<int:id>/edit/', views.edit_resource_request, name='edit_resource_request'),
    path('resource-requests/<int:id>/delete/', views.delete_resource_request, name='delete_resource_request'),
]
