from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from utils.SGPA_Calculation import *
from utils.pdfToDataframe import *

# Create your views here.
def home(request):
    return render(request, 'Home.html')
def login(request):
    return render(request,'Login.html')
def signup(request):
    return render(request, 'Signup.html')
def resultAnalysis(request):
    return render(request, 'Result Analysis.html')
def process_regular_sgpa(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        regular_class_file = request.FILES.get('regular_class')
        # Get the MIME type of the uploaded file
        file_mime_type = regular_class_file.content_type
        if file_mime_type == 'application/pdf':
            data=pdfToDataframe(regular_class_file)
            if isinstance(data, pd.DataFrame):
                SGPA_calculation(data)
                response = FileResponse(open('Result.xlsx', 'rb'))
                response['Content-Disposition'] = 'attachment; filename="Result.xlsx"'
                return response
            elif isinstance(data,str):
                return JsonResponse({'message': data},safe=False)
        return JsonResponse('Ok',safe=False)