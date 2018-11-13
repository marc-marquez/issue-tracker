"""
Creates the views for the:
    - index page
    - FAQ page
    - About page
    - Contact Us page
"""
from django.shortcuts import render

def get_index(request):
    """
    Returns index page
    :param request: The request type
    :return: index page
    """
    return render(request, 'index.html')

def get_faq(request):
    """
    Returns FAQ page
    :param request: The request type
    :return: FAQ page
    """
    return render(request, 'faq.html')

def get_about(request):
    """
    Returns the About Us page
    :param request: The request type
    :return: About Us page
    """
    return render(request, 'about.html')

def get_contact(request):
    """
    Returns the Contact Us page
    :param request: The request type
    :return: Contact Us page
    """
    return render(request, 'contact.html')
