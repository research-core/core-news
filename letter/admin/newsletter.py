from django.contrib import admin


class NewsletterAdmin(admin.ModelAdmin):
	list_display = ( 'newsletter_title', 'newsletter_datetime', 'newsletter_built', 'newsletter_sent', 'newsletter_sendfrom')
	list_filter = ('newsletter_active',)
	readonly_fields=('newsletter_external',)