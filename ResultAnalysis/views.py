from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from utils.SGPA_Calculation import *
from utils.pdfToDataframe import *
from .models import Gradepoints, Branchcodes
from utils.Styling_cells import *
from utils.branch_wise_analysis import *
from pandas import read_excel

# Create your views here.
def home(request):    
    return render(request, 'Home.html')
def login(request):
    return render(request, 'Login.html')
def signup(request):
    return render(request, 'Signup.html')
def resultAnalysis(request):
    branches=[]
    all_records = Branchcodes.objects.all()
    for i in all_records:
        branches.append(i.Abbrevation)
    return render(request, 'Result Analysis.html',{"branch_abbrevation":branches})
def process_regular_sgpa(request):
    grades=[]
    branch_codes=[]
    all_records = Gradepoints.objects.all()
    for i in all_records:
        grades.append([i.Grade,i.Points,i.Status,i.Presence])
    all_records = Branchcodes.objects.all()
    for i in all_records:
        branch_codes.append([i.Branch,i.Code,i.Abbrevation])
    if request.method == 'POST':
        # Get the uploaded file from the request
        regular_class_file = request.FILES.get('regular_class')
        selected_branch=request.POST.get('selected_branch')
        # Get the MIME type of the uploaded file
        file_mime_type = regular_class_file.content_type
        if file_mime_type == 'application/pdf':
            return_data=pdfToDataframe(regular_class_file)
            if isinstance(return_data, pd.DataFrame):
                value=SGPA_calculation(return_data,grades,branch_codes)
                if isinstance(value,str):
                    return JsonResponse({'message': value},safe=False)
                if selected_branch != None:
                    branchwise_analysis('Result.xlsx',selected_branch,grades)
                sgpa_styling("Result.xlsx")
                response = FileResponse(open('Result.xlsx', 'rb'))
                response['Content-Disposition'] = 'attachment; filename="Result.xlsx"'
                return response
            elif isinstance(return_data,str):
                return JsonResponse({'message': return_data},safe=False)
        elif file_mime_type=='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file_mime_type=='application/vnd.ms-excel':
            df=read_excel(regular_class_file)
            value=SGPA_calculation(df,grades,branch_codes)
            if isinstance(value,str):
                return JsonResponse({'message': value},safe=False)
            response = FileResponse(open('Result.xlsx', 'rb'))
            response['Content-Disposition'] = 'attachment; filename="Result.xlsx"'
            return response
        else:
            value='Please upload either excel or pdf only'
            return JsonResponse({'message': value},safe=False)