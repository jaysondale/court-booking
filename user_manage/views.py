from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomUserChangeForm
from django.contrib import messages

# Create your views here.

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
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print('saved')
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        print('not valid')

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)