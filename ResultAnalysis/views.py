from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
