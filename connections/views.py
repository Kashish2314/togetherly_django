from django.shortcuts import render

# Create your views here.
def connections(request):
    return render(request, 'connections/connections.html')