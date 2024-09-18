from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def user_reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            
            return redirect('heroes')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('heroes')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)

def user_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home_page')