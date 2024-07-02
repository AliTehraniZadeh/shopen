from django.shortcuts import render, redirect
import folium, geocoder
from .models import Search
from .forms import SearchForm
from django.http import HttpResponse

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SearchForm()
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('Your address is invalid')
    # Create Map Object
    m = folium.Map(location=[30, 57], zoom_start=2)
    folium.Marker([lat, lng], tooltip='click Here!', popup=country).add_to(m)
    # Get Html represntation of Map object
    m = m._repr_html_()
    context = {
        'm' : m,
        'form' : form
    }
    return render(request, 'index.html', context)