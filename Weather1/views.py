from django.shortcuts import render
import requests
from . models import City
from .forms import CityForm
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
   # city = 'Indore'
    err_msg=""
    msg=""
    msg_class=''
    if request.method=="POST":
        form=CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            ext_ctcnt=City.objects.filter(name=new_city).count()
            if(ext_ctcnt==0):
                r=requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                   err_msg="City does not Exist!!!"
            else:
                err_msg="City is already present!!"
        if(err_msg):
            msg=err_msg 
            msg_class='is-danger'
        else:
            msg="City added succesfully!!"
            msg_class='is-success'
    form=CityForm()
    cities=City.objects.all()
    weather_data=[]
    for city in cities:

        r=requests.get(url.format(city)).json()
        
        city_weather={
            'city' : city.name,
            'tempreature' : int((int(r['main']['temp'])-32)*(5/9)),
            'description' : r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context={'weather_data' : weather_data,
    'form' : form,
    'msg' : msg,
    'msg_class':msg_class,
    
    }
    return render(request, 'Weather1/Weather1.html',context) #returns the index.html template