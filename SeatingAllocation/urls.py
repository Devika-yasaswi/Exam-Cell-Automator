from django.urls import path
from . import views
urlpatterns= [
    path('Html/Seating Allocation.html',views.seatingAllocation, name='Seating Allocation'),
    path('Html/Attendance Sheet.html', views.attendanceSheet,name='Attendance Sheet')
]