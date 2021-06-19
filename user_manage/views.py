from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, forms
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def registrarionView(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created!')
            return redirect('login')

    context = {
        'form': form,
        'page_title': 'Registration'
    }
    return render(request, 'registration.html', context)
