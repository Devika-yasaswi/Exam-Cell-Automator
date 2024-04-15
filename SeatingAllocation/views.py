from django.shortcuts import render

def seatingAllocation(request):
    return render(request, 'Seating Allocation.html')
def attendanceSheet(request):
    return render(request, 'Attendance Sheet.html')
