from django.contrib import admin
from .models import User
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import requests
BASE_DIR = Path(__file__).resolve().parent.parent
env_path=os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)

def sendmail(modeladmin,request,queryset):
    for qs in queryset:
        url="https://api.openweathermap.org/data/2.5/weather?q="+qs.city+"&appid=f86e593293fdd8419fe416f811e01728"
        weather = requests.post(url)
        weather_dict=eval(weather.text)
        temp = round(weather_dict["main"]["temp"]-270)
        if temp <= 10:
            emoji="\U0001f976"
        elif temp > 10 and temp <= 20:
            emoji="\U0001f62c"
        elif temp > 20 and temp <= 30:
            emoji="\U0001f603"
        else:
            emoji="\U0001f975"
        subject = "Hi "+qs.username+", interested in our services "+emoji
        message = "The temperature in " +qs.city+ " is %d'C" %(temp)
        from_email = os.getenv("EMAIL_HOST_USER")
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [qs.email])
                try:
                    user = User.objects.get(email=qs.email)
                    if user:
                        user.sent = True
                        user.time = datetime.now()
                        user.save()
                except:
                    print("No email found")
                print(qs.email,"mail sent")

            except BadHeaderError:
                print(qs.email,"mail did not send")
        else:
            print("Validaiont error")

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','city','sent')
    actions = [sendmail]

admin.site.register(User, UserAdmin)