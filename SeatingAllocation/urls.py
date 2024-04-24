from django.urls import path
from . import views
urlpatterns= [
    path('Html/Seating Allocation.html',views.seatingAllocation, name='Seating Allocation'),
    path('Html/Attendance Sheet.html', views.attendanceSheet,name='Attendance Sheet'),
    path('process_seating_allocation/',views.process_Seating_Allocation, name='Seating Allocation Execution'),
    path('process_attendance_sheet/',views.process_Attendance_Sheet,name= "Attendance Sheet Execution")
]