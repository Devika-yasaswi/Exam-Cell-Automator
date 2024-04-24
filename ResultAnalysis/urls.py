from django.urls import path
from . import views
urlpatterns= [
    path('',views.home, name='Home'),
    path('Html/home.html',views.home, name='Home'),
    path('Html/login.html',views.login, name='Login'),
    path('Html/Signup.html',views.signup, name='Signup'),
    path('Html/Result Analysis.html', views.resultAnalysis, name='Result Analysis'),
    path('process_regular_sgpa/',views.process_regular_sgpa, name='Regular SGPA'),
    path('process_reval_sgpa/',views.process_reval_sgpa,name="Reval SGPA"),
    path('process_cgpa/',views.cgpa,name='CGPA')
    
]