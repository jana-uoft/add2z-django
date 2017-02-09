from django.shortcuts import render
from django.http import HttpResponse


context = {"STATIC_URL" : "https://storage.googleapis.com/add2z/classifieds/"}


def index(request):
	return HttpResponse("HOME PAGE FOR CLASSIFIED")