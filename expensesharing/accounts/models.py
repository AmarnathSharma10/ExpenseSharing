from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.CharField(max_length=10)
    email = models.EmailField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username+" "+self.name

# Create your models here.
