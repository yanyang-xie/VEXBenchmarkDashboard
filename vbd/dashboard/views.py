from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'dashboard/vod.html')

def about(request):
    return render(request, 'about.html')
