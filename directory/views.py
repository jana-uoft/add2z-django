from django.shortcuts import render


context = {"STATIC_URL" : "https://storage.googleapis.com/add2z/classifieds/"}

# Create your views here.
def index(request):
	return render(request, 'directory/coming_soon.html', context)