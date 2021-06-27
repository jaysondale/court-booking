from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages


def registration_view(request):
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
