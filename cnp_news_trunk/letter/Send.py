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

now = datetime.datetime.now()

new = Newsletter.objects.filter(newsletter_active=True).order_by('-newsletter_id')[0]

msg = MIMEText(smart_str(new.newsletter_html), 'html')
msg['Subject'] = 'Newsletter %s' % now
msg['From'] = 'ricardo.ribeiro@neuro.fchampalimaud.org'
msg['To'] = 'ricardo.ribeiro@neuro.fchampalimaud.org'

email = EmailMessage(msg['Subject'],new.newsletter_html, to=[msg['To']])
email.content_subtype = "html"
email.send()

new.newsletter_sent = now
newsletter_active = True