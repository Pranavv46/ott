from django.shortcuts import render

# Create your views here.

def adminlogin(request):
    return render(request,"adminlogin.html")
def forgotpassword(request):
    return render(request,"forgotpassword.html")
def home(request):
    return render(request,"home.html")
def editmovie(request):
    return render(request,"editmovie.html")
def edituser(request):
    return render(request,"edituser.html")