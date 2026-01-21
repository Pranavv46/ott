
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.db import models 
from django.core.validators import FileExtensionValidator

from django.conf import settings



class UserManager(BaseUserManager): 
      def create_user(self, email, password=None): 
            if not email: 
                 raise ValueError("Users must have an email address") 
            email = self.normalize_email(email) 
            user = self.model(email=email) 
            user.set_password(password) 
            user.save(using=self._db) 
            return user 
 
      def create_superuser(self, email, password): 
        user = self.create_user(email, password) 
        user.is_admin = True 
        user.is_superuser = True 
        user.save(using=self._db) 
        return user 
 
class User(AbstractBaseUser): 
    email = models.EmailField(unique=True) 
    name = models.CharField(max_length =255) 
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 
    objects = UserManager() 
 
    USERNAME_FIELD = 'email'

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    poster = models.FileField(
        upload_to='posters/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
        null=True,   
        blank=True    
    )
    video_file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv'])],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
    
class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} watched {self.movie.title} on {self.watched_at}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} added {self.movie.title} to watchlist on {self.added_at}"
