from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    name = models.CharField(max_length=100, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email Address')
    position = models.CharField(max_length=100, verbose_name='Position')
    added_on = models.DateTimeField(default=timezone.now, verbose_name='Date Added')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class DynamicData(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='dynamic_data', verbose_name='User Profile')
    data = models.JSONField(default=dict, verbose_name='Dynamic Data')

    class Meta:
        verbose_name = 'Dynamic Data'
        verbose_name_plural = 'Dynamic Data'
