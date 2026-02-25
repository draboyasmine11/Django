from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms_auth import CustomUserCreationForm, EmailOrUsernameAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f"Bienvenue {form.get_user().username}!")

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = EmailOrUsernameAuthenticationForm()
     
    return render(request, 'school/login.html', {'form': form, 'next': request.GET.get('next', '')})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'school/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'school/profile.html', {'user': request.user})
