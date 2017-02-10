from letter.models import Subject, Message, Newsletter, MessageScope
from letter.admin.message import MessageAdmin
from letter.admin.subject import SubjectAdmin
from letter.admin.newsletter import NewsletterAdmin
from django.contrib import admin

admin.site.register(Subject,SubjectAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(MessageScope)