from django.contrib.auth import logout

from django.shortcuts import render

from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from django.urls import reverse


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data['password'])
            user.save()
            context = {
                'user':user
            }
            return render(request, 'registration/register_done.html', context)
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'
    extra_context = {'title': "Авторизация"}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))