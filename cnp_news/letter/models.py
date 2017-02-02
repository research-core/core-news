from django.db import models
from django.db.models import Q

import datetime

class Subject(models.Model):
    subject_id = models.AutoField('Id', primary_key=True)
    subject_title = models.CharField(max_length=200)
    subject_text = models.TextField('Text', blank=True, null=True,)
    subject_active = models.BooleanField('Active')
    subject_order = models.IntegerField('Order')

    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.subject_title

class Newsletter(models.Model):
    newsletter_id = models.AutoField('Id', primary_key=True)
    newsletter_title = models.CharField(max_length=200)
    newsletter_html = models.TextField('HTML')
    newsletter_datetime = models.DateTimeField('Date', blank=True, null=True,)
    newsletter_built = models.DateTimeField('Built date')
    newsletter_sent = models.DateTimeField('Sent date', blank=True, null=True,)
    newsletter_active = models.BooleanField('Active')
    newsletter_sendfrom = models.CharField('Send from',max_length=100, blank=True, null=True,)
    newsletter_external = models.BooleanField('External newsletter')

    def __unicode__(self):
        return str(self.newsletter_id)

# Whether the message should be included in the internal, external or both newsletters
class MessageScope(models.Model):
    message_scope_id = models.AutoField('Id', primary_key=True)
    message_scope = models.CharField(max_length=250)

    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return str(self.message_scope)

class Message(models.Model):
    message_id          = models.AutoField('Id', primary_key=True)
    message_event       = models.BooleanField('Send an email to everyone, one day before the event', default=True)
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

    newsletter_start_vpdt   = models.ForeignKey('Newsletter', blank=True, null=True, related_name='Start publish newsletter')
    newsletter_end_vpdt     = models.ForeignKey('Newsletter', blank=True, null=True, related_name='End publish newsletter ')

    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.message_title