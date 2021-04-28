from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse, HttpResponse


def home_page(request):
    return render(request, 'home.html', {})


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
