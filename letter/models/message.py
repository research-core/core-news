from django.db import models

class Message(models.Model):
	message_id          = models.AutoField('Id', primary_key=True)
	message_event       = models.NullBooleanField('Send an email to everyone, one day before the event', default=True)
	message_pubstart    = models.DateField('Start publish date', blank=True, null=True, help_text="If you let this field empty, the message will be sent from now to 'End publish date'." )
	message_pubend      = models.DateField('End publish date', blank=True, null=True, help_text="If you let this field empty, the message will be sent only one time." )
	message_order       = models.IntegerField('Order', blank=True, null=True, help_text="Order in the email." )
	subject             = models.ForeignKey('Subject')
	message_title       = models.CharField(max_length=200)
	message_img         = models.ImageField('Image', upload_to="uploads/message/", max_length=300, blank=True)
	message_datetime    = models.DateTimeField('Date', blank=True, null=True, help_text="Example: you can put here a date of an event." )
	message_location    = models.CharField('Location', max_length=200, blank=True, null=True, help_text="Example: you can put here the location of an event." )
	message_text        = models.TextField('Text')
	message_scope       = models.ForeignKey('MessageScope')

	newsletter_start_vpdt = models.ForeignKey('Newsletter', blank=True, null=True, related_name='Start publish newsletter+')
	newsletter_end_vpdt   = models.ForeignKey('Newsletter', blank=True, null=True, related_name='End publish newsletter+')

	def __unicode__(self): return self.message_title