from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from .models import User

from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from .models import Movie
from .serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

def adminlogin(request):
    return render(request,"adminlogin.html")
def forgotpassword(request):
    return render(request,"forgotpassword.html")
def home(request):
    return render(request,"home.html")
def editmovie(request):
    return render(request,"editmovie.html")
def edituser(request):\
    return render(request,"edituser.html")
def addmovie(request):
    return render(request,"addmovie.html")
def userhistory(request):
    return render(request,"userhistory.html")
def view(request):
    return render(request,"view.html")
def reports(request):
    return render(request,"reports.html")
 
@api_view(['POST'])
@permission_classes((AllowAny,))

def Signup(request):
        email  = request.data.get("email")
        password = request.data.get("password")

        
       
        name = request.data.get("name")
        if not name or not email or not password:
            return Response({'message':'All fields are required'})
        if User.objects.filter(email=email).exists():
            return  JsonResponse({'message':'Email already exist'})
        user = User.objects.create_user(email=email,password=password)
        user.name = name
        user.save()
        return JsonResponse({'message':'user created successsfully'} ,status = 200)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    print(email,password)
    if email is None or password is None:
        return Response({'error': 'Please provide email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def movies(request):

    # GET → list all movies
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    # POST → create movie
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
