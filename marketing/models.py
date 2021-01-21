from django.db import models

# Create your models here.

class Singup(models.Model):
    email = models.EmailField()
    timestime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email