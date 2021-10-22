from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import (CustomUser, UserLoginForm,
                    UserRegistrationForm,
                    UserPwdChangeForm,
                    UserPwdResetForm)

# Create your views here.


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        return super().form_valid(form)


class UserRegistrationView(CreateView):
    model = CustomUser
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:login')


class UserPwdChangeView(PasswordChangeView):
    template_name = 'accounts/pwd_change.html'
    form_class = UserPwdChangeForm
    success_url = reverse_lazy('app_users:pwd_change')

    def get_form_kwargs(self):
        kwargs = super(UserPwdChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        context = self.get_context_data()
        context['message'] = "Your Password has been changed successfully!"
        return render(self.request, self.template_name, context)


class UserPwdResetView(FormView):
    template_name = 'accounts/pwd_reset.html'
    form_class = UserPwdResetForm
    success_url = reverse_lazy('app_users:pwd_reset')

    def form_valid(self, form):
        # Get user object
        user = CustomUser.objects.get(
            email=form.cleaned_data.get('email'))

        # Set new password and save
        user.set_password(form.cleaned_data.get('new_password1'))
        user.save()

        context = self.get_context_data()
        context['message'] = "Your Password has been changed successfully!"
        return render(self.request, self.template_name, context)
