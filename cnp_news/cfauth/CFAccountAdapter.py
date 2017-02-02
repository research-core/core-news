from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from allauth.utils import (import_attribute, email_address_exists, valid_email_or_none)
from allauth.account.utils import user_email, user_username, user_field
from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account import app_settings as account_settings
from allauth.account.app_settings import EmailVerificationMethod
from allauth.socialaccount import app_settings
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import logout
from django.conf import settings

from allauth.utils import resolve_url

class CFSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        email = user_email(sociallogin.account.user)
        try:
            u = User.objects.get(email=email)
            sociallogin.account.user = u
            u = super(CFSocialAccountAdapter,self).save_user(request, sociallogin, form)
        except:
            try:
                u = super(CFSocialAccountAdapter,self).save_user(request, sociallogin, form)
            except:
                u = User.objects.get(email=email)
            u.username = email.replace('@neuro.fchampalimaud.org', '')
            u.set_password( User.objects.make_random_password(length=50) )
            u.is_staff = True

        g = Group.objects.get(name=settings.PROFILE_GUEST)
        u.groups.add(g)        
        u.save()
        return u
        


    def is_auto_signup_allowed(self, request, sociallogin):
        # If email is specified, check for duplicate and if so, no auto signup.
        email = user_email(sociallogin.account.user)
        return email.endswith('@neuro.fchampalimaud.org')

    def is_open_for_signup(self, request, sociallogin):
        email = user_email(sociallogin.account.user)
        return email.endswith('@neuro.fchampalimaud.org')


class CFAccountAdapter(DefaultAccountAdapter):



    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed on the db
        """
        if email_address.email.endswith('@neuro.fchampalimaud.org') or email_address.email.endswith('@fundacaochampalimaud.pt'):
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()

    def login(self, request, user):
        from django.contrib.auth import login

        if not hasattr(user, 'backend'): user.backend = "allauth.account.auth_backends.AuthenticationBackend"
        if user.is_superuser or user.email.endswith('@fundacaochampalimaud.pt') or user.email.endswith('@neuro.fchampalimaud.org'): 
            login(request, user)

    def save_user(self, request, user, form, commit=True):
        if form['email'].value().endswith('@fundacaochampalimaud.pt') or form['email'].value().endswith('@neuro.fchampalimaud.org'): 
            user = super( CFAccountAdapter, self ).save_user(request, user, form, commit=True)
            user.is_staff = True
            g = Group.objects.get(name=settings.PROFILE_GUEST)
            user.groups.add(g)
            user.save()
        return user

    def get_login_redirect_url(self, request):
        url = getattr(settings, "LOGIN_REDIRECT_URLNAME", None)
        if request.user.is_authenticated() and url:
            warnings.warn("LOGIN_REDIRECT_URLNAME is deprecated, simply"
                          " use LOGIN_REDIRECT_URL with a URL name",
                          DeprecationWarning)
        else:
            url = settings.LOGIN_REDIRECT_URL
        return resolve_url(url)

def get_adapter():
    return import_attribute(app_settings.ADAPTER)()
