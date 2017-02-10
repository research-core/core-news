from letter.models import Subject, Message, Newsletter, MessageScope
from django.contrib import admin

class SubjectAdmin(admin.ModelAdmin):
	list_display = ( 'subject_title', 'subject_active', 'subject_order')
	list_filter = ('subject_active', )


class MessageAdmin(admin.ModelAdmin):
    list_display = ( 'message_title', 'subject', 'message_pubstart', 'message_pubend', 'message_order','message_event','message_datetime', 'message_scope')
    list_filter = ('subject','message_event', )
    search_fields = ['message_title','message_text']
    exclude=["newsletter_start_vpdt","newsletter_end_vpdt"]

    radio_fields = {
        'message_scope': admin.HORIZONTAL,
    }

    fieldsets = [
        ('Content', {
                'classes': ('suit-tab suit-tab-Content',),
                'fields': ['message_event', 'subject','message_title','message_text', 'message_scope' ]
            }),
        ('Optinal content',{
                'classes': ('suit-tab suit-tab-OptinalContent',),
                'fields': ['message_img','message_location','message_datetime',],
            }),
        ('Publishing information', {
                'classes': ('suit-tab suit-tab-PublishingInfo',),
                'fields': ['message_pubstart', 'message_pubend', 'message_order',]
            }),
    ]

    suit_form_tabs = [
        (u'Content', u'Content'),
        (u'OptinalContent', u'Optinal content'),
        (u'PublishingInfo', u'Publishing information'),
    ]

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ( 'newsletter_title', 'newsletter_datetime', 'newsletter_built', 'newsletter_sent', 'newsletter_sendfrom')
    list_filter = ('newsletter_active',)
    readonly_fields=('newsletter_external',)
    
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(MessageScope)