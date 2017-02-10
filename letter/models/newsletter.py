from django.db import models

class Newsletter(models.Model):
	newsletter_id 		= models.AutoField('Id', primary_key=True)
	newsletter_title 	= models.CharField(max_length=200)
	newsletter_html 	= models.TextField('HTML')
	newsletter_datetime = models.DateTimeField('Date', blank=True, null=True,)
	newsletter_built 	= models.DateTimeField('Built date')
	newsletter_sent 	= models.DateTimeField('Sent date', blank=True, null=True,)
	newsletter_active 	= models.BooleanField('Active')
	newsletter_sendfrom = models.CharField('Send from',max_length=100, blank=True, null=True,)
	newsletter_external = models.BooleanField('External newsletter')

	def __unicode__(self): return str(self.newsletter_id)