from django.shortcuts import render

# Create your views here.
def circle (request):
    return render(request, 'circlemaker/circle.html')

def line (request):
    return render(request, 'circlemaker/line.html')

def home (request):
    return render(request, 'circlemaker/index.html')