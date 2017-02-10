from django.contrib import admin

class SubjectAdmin(admin.ModelAdmin):
	list_display = ( 'subject_title', 'subject_active', 'subject_order')
	list_filter = ('subject_active', )