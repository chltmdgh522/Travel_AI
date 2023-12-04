from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
# users/models.py


class TravelResponse(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    departure_date = models.DateField(null=True)
    arrival_date = models.DateField(null=True)
    companion = models.CharField(max_length=255)
    travel_style = models.CharField(max_length=255)
    age = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} - {self.country} - {self.duration} -{self.departure_date} - {self.arrival_date} - {self.companions} - {self.travel_style} - {self.travel_schedule}'


class TravelDestination(models.Model):
    name = models.CharField(max_length=255)
    keyword = models.TextField()
    latitude = models.FloatField(null=True, blank=True)  # 추가: 위도
    longitude = models.FloatField(null=True, blank=True)  # 추가: 경도
    country = models.CharField(max_length=255, null=True, blank=True)  # 추가: 나라

    def __str__(self):
        return self.name
class SurveyData(models.Model):
    country = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    preference = models.IntegerField()
    gender = models.CharField(max_length=10)
    companion = models.CharField(max_length=255)
    age = models.CharField(max_length=255)




