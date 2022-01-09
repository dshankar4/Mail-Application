from django.db import models

class User(models.Model):
    cityChoices = (('Mumbai','Mumbai'),('Delhi','Delhi'),('Chennai','Chennai'),('Bengaluru','Bengaluru'),('Kolkata','Kolkata'))
    email = models.EmailField()
    username = models.CharField(max_length=100)
    city = models.CharField(max_length=20,default="Mumbai",choices=cityChoices)
    sent = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now=True)