from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import  UserTaskAccount
from django.shortcuts import get_object_or_404, redirect
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login , update_session_auth_hash
from django.utils.decorators import method_decorator
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_mail_to_user(user, subject, template, **kwargs):
    user_first_name = user.first_name
    user_last_name = user.last_name
    kwargs['user_first_name'] = user_first_name
    kwargs['user_last_name'] = user_last_name

    html_content = render_to_string(template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, to=[user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()



class UserRegistrationView(FormView):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
                self.request, "Welcome.")  # Change 'request' to 'self.request'
        send_mail_to_user(self.request.user, "Welcome", "welcomeEmail.html")
        return super().form_valid(form)

    


class UserLoginView(LoginView):
    template_name = 'user_login.html'

    def get_success_url(self):
        messages.success(self.request, 'Successfully logged in')
        return reverse_lazy('home')

from django.shortcuts import HttpResponseRedirect


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Successfully logged out')
            logout(self.request)
        return reverse_lazy('home')
    


class UserTaskAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        return render(request, self.template_name, {'form': form})
    
@login_required
def ProfileData(request):
    print(request)
    data_pending = None
    data_accepted = None

    if hasattr(request.user, 'account'):
        user_account = request.user.account

        if hasattr(user_account, 'user'):
            user = user_account.user

            data_pending = BookedHotelModel.objects.filter(user=user, buy_status='PENDING')
            data_accepted = BookedHotelModel.objects.filter(user=user, buy_status='Accepted')

        
    return render(request, 'profile.html', {'data_pending': data_pending, 'data_accepted': data_accepted})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
    return render(request, 'update_profile.html', {'form' : profile_form})


def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : form})
