from django.urls import path
from . import views
urlpatterns= [
    path('Html/Seating Allocation.html',views.seatingAllocation, name='Home'),
]