from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from utils.seating_Allocation import create_pdf
from utils.attendance_sheet import generate_attendance_sheet
from utils.pdfToDataframe import *
def seatingAllocation(request):
    return render(request, 'Seating Allocation.html')
def attendanceSheet(request):
    return render(request, 'Attendance Sheet.html')
def process_Seating_Allocation(request):
    portal_data=request.FILES.get('portal_data')
    seating_plan=request.FILES.get('seating_plan')
    file_mime_type=portal_data.content_type
    if file_mime_type == 'application/pdf':
        return_data=pdfToDataframe(portal_data)
        create_pdf("seating Arrangement.pdf",return_data,seating_plan)
        response = FileResponse(open('seating Arrangement.pdf', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="seating Arrangement.pdf"'
        return response
def process_Attendance_Sheet(request):
    portal_data=request.FILES.get('portal_data')
    seating_plan=request.FILES.get('seating_plan')
    file_mime_type=portal_data.content_type
    if file_mime_type == 'application/pdf':
        return_data=pdfToDataframe(portal_data)
        generate_attendance_sheet("Attendance Sheet.pdf",return_data,seating_plan)
        response = FileResponse(open('Attendance Sheet.pdf', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="Attendance Sheet.pdf"'
        return response