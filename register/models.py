from django.db import models
from django.contrib.auth.models import User


# user profile to store ip info for users
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ipAddress = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username
