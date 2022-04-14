from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from .models import User


def registrationView(request):
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

@login_required
def profileView(request):
    if request.method == 'POST':
        print('is post')
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        print('not valid')

    context = {
        'u_form': u_form,
        'page_title': 'My Profile'
    }
    return render(request, 'profile.html', context)

def deleteView(request, pk):
    obj = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        obj.delete()
    context = {
        "object": obj
    }
    return render(request, "delete.html", context)

def defaultView(request):
    if request.user.is_authenticated:
        return redirect('calendar')
    else:
        return redirect('login')

