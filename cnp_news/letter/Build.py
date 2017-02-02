import sys,os
sys.path.append(os.path.dirname( os.path.dirname(os.getcwdu() ) ) )
os.environ['DJANGO_SETTINGS_MODULE'] ='newsletter.settings'
from django.core.management import setup_environ
from newsletter import settings
setup_environ(settings)


import new
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import loader, Context
from letter.models import Subject, Newsletter
from django.core.paginator import Paginator
from django.utils import translation
from itertools import *
from email.mime.text import MIMEText
from django.utils.encoding import smart_str, smart_unicode
from django.core.mail import EmailMessage

import datetime
import smtplib



