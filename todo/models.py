from datetime import date
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class list(models.Model):
    title= models.CharField(max_length=100)
    description= models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True,blank=True)
    impo= models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
