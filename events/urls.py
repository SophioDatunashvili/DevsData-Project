from django.urls import path
from .views import EventListAPIView, EventDetailAPIView, event_list, \
    event_detail, ReservationList, ReservationDetail, \
    reservation_detail, delete_reservation, reservation_deleted
from django.urls import re_path

urlpatterns = [
    path('api/events/', EventListAPIView.as_view(), name='event-list-api'),
    path('api/events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail-api'),
    path('events/', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('api/reservations/', ReservationList.as_view(), name='reservation-list'),
    path('api/reservations/<int:pk>/', ReservationDetail.as_view(), name='reservation-detail-api'),
    path('events/<int:pk>/<uuid:reservation_code>/', reservation_detail, name='reservation_detail'),
    path('delete-reservation/', delete_reservation, name='delete_reservation'),
    path('reservation-deleted/', reservation_deleted, name='reservation_deleted'),


]
