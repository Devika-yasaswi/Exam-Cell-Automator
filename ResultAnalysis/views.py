from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from utils.SGPA_Calculation import *
from utils.pdfToDataframe import *
from .models import Gradepoints, Branchcodes
from utils.Styling_cells import *
from utils.branch_wise_analysis import *
from utils.revaluation import reval_calculation
from utils.CGPA_calculation import cgpa_calculation,objects_list
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
            if selected_branch != None:
                branchwise_analysis('Result.xlsx',selected_branch,grades)
            sgpa_styling("Result.xlsx")
            response = FileResponse(open('Result.xlsx', 'rb'))
            response['Content-Disposition'] = 'attachment; filename="Result.xlsx"'
            return response
        else:
            value='Please upload either excel or pdf only'
            return JsonResponse({'message': value},safe=False)
def process_reval_sgpa(request):
    grades=[]
    branch_codes=[]
    all_records = Gradepoints.objects.all()
    for i in all_records:
        grades.append([i.Grade,i.Points,i.Status,i.Presence])
    all_records = Branchcodes.objects.all()
    for i in all_records:
        branch_codes.append([i.Branch,i.Code,i.Abbrevation])
    if request.method == 'POST':
        supply_result_file = request.FILES.get('supply_class')
        gpa_file=request.FILES.get("supply_gpa_class")
        file_mime_type = supply_result_file.content_type
        if file_mime_type == 'application/pdf':
            return_data=pdfToDataframe(supply_result_file)
            if isinstance(return_data, pd.DataFrame):
                reval_calculation(gpa_file,return_data,grades,branch_codes)
                sgpa_styling("Result.xlsx")
                response = FileResponse(open('Result.xlsx', 'rb'))
                response['Content-Disposition'] = 'attachment; filename="Result.xlsx"'
                return response
            
def cgpa(request):
    branch_codes=[]
    all_records = Branchcodes.objects.all()
    for i in all_records:
        branch_codes.append([i.Branch,i.Code,i.Abbrevation])
    sem_files=[]
    for i in range(8):
        sem_files.append(request.FILES.get('cgpa_class'+str(i+1)))
        if sem_files[i]!=None:
            cgpa_calculation(sem_files[i],i+1)
    for obj in objects_list:
        obj.cgpa_cal()
    with pd.ExcelWriter("Result.xlsx",engine='openpyxl',mode='w') as output:
        for i in range(len(objects_list)):
            for j in range(len(branch_codes)):
                if objects_list[i].branch==branch_codes[j][1]:
                    objects_list[i].cgpa_df.to_excel(output,sheet_name=branch_codes[j][2],index=False)
    cgpa_styling("Result.xlsx")
    response = FileResponse(open('Result.xlsx', 'rb'))
    response['Content-Disposition'] = 'attachment; filename="Result.xlsx"'
    return response