from django.shortcuts import render
from django.http import HttpResponse

def home(response):
    return HttpResponse("<h1>Resto Kans</h1>")

        