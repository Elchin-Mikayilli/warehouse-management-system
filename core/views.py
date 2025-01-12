


from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Ensure the template name is exactly 'home.html'
