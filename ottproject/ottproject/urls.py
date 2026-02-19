"""
URL configuration for ottproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie import views


from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlogin/', views.adminlogin ,name='adminlogin'),
    path('forgotpassword/', views.forgotpassword ),
    path('home/', views.home ),
    path('editmovie/', views.editmovie, name="editmovie" ),
    path('edituser/', views.edituser ),
    path('addmovie/', views.addmovie, name="addmovie" ),  
    path('userhistory/', views.userhistory ),
    
    path('reports/', views.reports, name='reports' ),


     path('signup/',views.Signup,name='signup_api'),
     path('login/', views.userlogin, name='login_api'),

     path('api/movies/', views.movies, name='movies_api'),

     path('api/watch-history/', views.add_watch_history, name='watch-history'),

     path('api/watchlist/', views.watchlist, name='watchlist'),
     path('api/movies/<int:pk>/', views.MovieDetail, name='movie-detail'),
     
     path('movie/<int:id>/', views.view, name='movie_page'),




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)