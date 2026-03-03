from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .models import User, Movie, WatchHistory, Watchlist
from .serializers import MovieSerializer, WatchHistorySerializer, WatchlistSerializer


# ==========================
# ADMIN LOGIN / LOGOUT
# ==========================

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_admin:
            login(request, user)
            return redirect('/home/')

    return render(request, "adminlogin.html")


def admin_logout(request):
    logout(request)
    return redirect('/adminlogin/')


# ==========================
# ADMIN PROTECTED PAGES
# ==========================

@never_cache
@login_required(login_url='/adminlogin/')
def home(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {'movies': movies})


@never_cache
@login_required(login_url='/adminlogin/')
def addmovie(request):
    return render(request, "addmovie.html")


@never_cache
@login_required(login_url='/adminlogin/')
def editmovie(request):
    return render(request, "editmovie.html")


@never_cache
@login_required(login_url='/adminlogin/')
def edituser(request):
    return render(request, "edituser.html")


@never_cache
@login_required(login_url='/adminlogin/')
def userhistory(request):
    return render(request, "userhistory.html")


@never_cache
@login_required(login_url='/adminlogin/')
def reports(request):
    return render(request, "reports.html")


@never_cache
@login_required(login_url='/adminlogin/')
def trending_movies(request):
    movies = Movie.objects.all().order_by('-release_date')[:10]
    return render(request, 'trending.html', {'movies': movies})


@never_cache
@login_required(login_url='/adminlogin/')
def movie_page(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "view.html", {"movie": movie})


def forgotpassword(request):
    return render(request, "forgotpassword.html")


# ==========================
# USER API SECTION (React)
# ==========================

@api_view(['POST'])
@permission_classes([AllowAny])
def Signup(request):
    email = request.data.get("email")
    password = request.data.get("password")
    name = request.data.get("name")

    if not name or not email or not password:
        return Response({'message': 'All fields are required'})

    if User.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})

    user = User.objects.create_user(email=email, password=password)
    user.name = name
    user.save()

    return JsonResponse({'message': 'User created successfully'}, status=200)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def userlogin(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None:
        return Response({'error': 'Please provide email and password'},
                        status=HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)
    except:
        return Response({"error": "Something went wrong"}, status=400)


# ==========================
# MOVIES API
# ==========================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def movies(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MovieDetail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_watch_history(request):
    serializer = WatchHistorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"message": "Watch history saved"}, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watchlist(request):

    if request.method == 'GET':
        qs = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = WatchlistSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            movie = serializer.validated_data['movie']

            if Watchlist.objects.filter(user=request.user, movie=movie).exists():
                return Response({"error": "Movie already in watchlist"}, status=400)

            serializer.save()
            return Response({"message": "Added"}, status=201)

        return Response(serializer.errors, status=400)