from django.db import models

class Message(models.Model):

	publish_start    = models.DateField('Start publish date', blank=True, null=True)
	publish_end      = models.DateField('End publish date', blank=True, null=True)
	first_newsletter = models.ForeignKey('plugins.core-news.letter.models.newsletter.Communication', blank=True, null=True, related_name='firsts_msgs', on_delete=models.CASCADE)
	last_newsletter  = models.ForeignKey('plugins.core-news.letter.models.newsletter.Communication', blank=True, null=True, related_name='lasts_msgs', on_delete=models.CASCADE)

	subject = models.ForeignKey('Subject')
	order   = models.IntegerField('Order', blank=True, null=True)
	name 	= models.CharField("Name", max_length=200)
	image   = models.ImageField('Image', upload_to="uploads/message/", max_length=300, blank=True)
	date    = models.DateTimeField('Date', blank=True, null=True)
	text 	= models.TextField('Text', null=True, blank=True)

	is_event = models.BooleanField('Is an event', default=True)
	location = models.CharField('Location', max_length=200, blank=True, null=True)
	start 	 = models.DateTimeField('Start', blank=True, null=True)
	end 	 = models.DateTimeField('End', blank=True, null=True)

	mailing_list = models.ForeignKey('MailingList', on_delete=models.CASCADE)

	def __str__(self):
		return self.message_title