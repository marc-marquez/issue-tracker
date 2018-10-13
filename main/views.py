from django.shortcuts import render

def get_index(request):
    return render(request, 'index.html')

def get_faq(request):
    return render(request, 'faq.html')

def get_about(request):
    return render(request, 'about.html')