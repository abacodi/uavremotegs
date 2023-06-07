from audioop import reverse
from email.policy import default
import imp
from turtle import position

from django.urls import reverse_lazy
from .forms import AccessForm, SignUpForm, PasswordResetRequestForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.validators import validate_email
from django.views.generic.edit import FormView
from django.db.models.query_utils import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from docDb import settings

from .tokens import account_activation_token
from .models import GeneralSettings

import requests


# Variable for debug
debug = False  # Only one log is necessary thanks to the cookies


# User information
class UserView(TemplateView):
    template_name = 'Generic/user_info.html'  # The template

# Home view
class HomeView(TemplateView):
    template_name = 'Generic/home_page.html'  # The template

    @staticmethod
    def get_news(request):
        # Render the template
        return render(request, HomeView.template_name)

    @staticmethod
    def permission_denied(request):
        return render(request, 'Generic/permission_denied.html')

# Access view
def access(request):
    if not debug and not request.user.id:
        if request.method == "POST":  # When button is pressed
            # The form
            form = AccessForm(data=request.POST)

            # Check that the form is valid: the captcha field will automatically check the input
            if form.is_valid():
                #reCAPTCHA validation
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()

                if result['success']:
                    # Get the username and password
                    usr_name = request.POST['username']
                    pwd = request.POST['password']

                    # Check the password in the database
                    user = authenticate(username=usr_name, password=pwd)

                    if user is not None:
                        # Make the actual login to the django system
                        login(request, user)

                        # Redirect to show all the users
                        return redirect('Generic:home')
                    else:
                        # Raise an error
                        return render(request, 'Generic/access_form.html', {'form': form, 'error': True, 'recaptcha_site_key':settings.RECAPTCHA_SITE_KEY})
                        # raise Http404("Incorrect user authentication")
            else:  # Bootstrap should avoid this
                return render(request, 'Generic/access_form.html', {'form': form, 'error': True, 'recaptcha_site_key':settings.RECAPTCHA_SITE_KEY})
                # raise Http404("Form not filled correctly or incorrect user authentication")
        else:  # First time
            form = AccessForm()
    else:
        # Redirect to show all the users
        return redirect('Generic:home')

    # Render the form
    return render(request, 'Generic/access_form.html', {'form': form, 'error': True, 'recaptcha_site_key':settings.RECAPTCHA_SITE_KEY})


# Logout
def logout_view(request):
    # First logout
    logout(request)
    # Then, redirect to the access page
    return redirect('Generic:access')


# Signup
def signup_view(request):
    request.POST = request.POST.copy()
    try:
        default_hours = request.POST['default_hours']
    except:
        default_hours = 8
    request.POST['default_hours'] = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            ######
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your UAV ABA AirLink GS Account'
            message = render_to_string('Generic/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()

            messages.success(request, 'Please confirm your email address to complete the registration.')
    else:  # First time
        form = SignUpForm()
    return render(request, 'Generic/signup.html', {'form': form})

def permissions_view(request):
    return render(request, 'Generic/permissions.html', {})

# To reset password
class ResetPasswordRequest(FormView):
    template_name = "Generic/reset_pwd.html"  # code for template is given below the view's code
    success_url = reverse_lazy('Generic:reset')
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        """
        This method here validates the if the input is an email address or not. Its return type is boolean,
        True if the input is a email address or False if its not.
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        """
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]

            if self.validate_email_address(data) is True:  # uses the method written above
                """If the input is an valid email address, then the following code will lookup for users associated 
                with that email address. If found then an email will be sent to the address, else an error message 
                will be printed on the screen. """
                associated_users = User.objects.filter(Q(email=data) | Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        message = render_to_string('Generic/password_reset_email.html', {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': "ABA's UAV Remote GS",
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        })
                        subject = "Reset Your ABA's UAV Remote Ground Station Password"
                        email = EmailMessage(
                            subject, message, to=[user.email]
                        )
                        email.send()
                    result = self.form_valid(form)
                    messages.success(request,
                                     'An email has been sent to ' + data + ". Please check its inbox to continue "
                                                                           "reseting password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result
            else:
                """If the input is an username, then the following code will lookup for users associated with that 
                user. If found then an email will be sent to the user's address, else an error message will be 
                printed on the screen. """
                associated_users = User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        message = render_to_string('Generic/password_reset_email.html', {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'your site',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        })
                        subject = "Reset Your UAV ABA's UAV Remote GS Password"
                        email = EmailMessage(
                            subject, message, to=[user.email]
                        )
                        email.send()
                    result = self.form_valid(form)
                    messages.success(request,
                                     'Email has been sent to ' + data + "'s email address. Please check its inbox to "
                                                                        "continue reseting password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'This username does not exist in the system.')
                return result
        else:
            messages.error(request, 'Invalid Input')
            return self.form_invalid(form)


# Password reset
class PasswordResetConfirmView(FormView):
    template_name = "Generic/reset_pwd.html"
    success_url = reverse_lazy('Generic:access')
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = User
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


# Waiting for activation
class ActivationView(ListView):
    template_name = 'Generic/account_activation_email.html'  # The template


# To activate
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Add to database
        user.is_active = True
        user.save()

        # Login
        return redirect('Generic:access')
    else:
        return render(request, 'Generic/account_activation_invalid.html')