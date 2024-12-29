from asyncio.windows_events import NULL
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
import utm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
import requests
import json
import urllib
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import paho.mqtt.client as mqtt
from django.conf import settings


# Create your views here.
@csrf_exempt
def service_worker(request):
    sw_path = settings.BASE_DIR / "templates/google" / "serviceworker.js"
    response = HttpResponse(open(sw_path).read(), content_type='application/javascript')
    return response


@csrf_exempt
def home(request):
    context = {}
    return render(request, 'google/home.html', context)


@csrf_exempt
def map(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
    }
    return render(request, 'google/map.html', context)


@csrf_exempt
def mydata(request):
    result_list = list(CMVData.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('latitude',
                               'longitude',
                               'cmv'
                               ))
    f = []
    for i, j in zip(result_list, range(len(result_list))):
        ne = utm.from_latlon(float(i['latitude']), float(i['longitude']))
        a = {'latitude': i['latitude'], 'longitude': i['longitude'], 'Northing': ne[0], 'Easting': ne[1],
             'CMV': i['cmv']}
        f.append(a)
    return JsonResponse(f, safe=False)


@csrf_exempt
def your_view(request):
    if request.method == "POST":
        da = CMVData.objects.all()[10]
        da.cmv = request.POST['data']
        da.save()
        return HttpResponse(da)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'google/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'google/password_reset.html'
    email_template_name = 'google'
    subject_template_name = 'google/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('google-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'google/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('google-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'google/profile.html', {'user_form': user_form, 'profile_form': profile_form})


def publish_message(request):
    request_data = json.loads(request.body)
    # rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': request_data})


def mqtt_check(request):
    if request.method == "GET":
        path = r"C:\Users\ajinf\PycharmProjects\Maps\google\data.json"
        with open(path, 'r') as openfile:
            json_object = json.load(openfile)

        return JsonResponse(json_object, safe=False)
