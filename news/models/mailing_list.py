from django.db import models
from django.db.models import Q
from django.utils import timezone
from news.models import Message

class MailingList(models.Model):

	SEND_FREQUENCY = [
		('D', 'Daily'),
		('W', 'Weekly'),
		('M', 'Monthly'),
	]

	name     = models.CharField('Name', max_length=150, unique=True)
	subject  = models.CharField('Email subject', max_length=255)
	email    = models.EmailField('Email', max_length=255)
	template = models.ForeignKey('Template', on_delete=models.CASCADE)

	reminder_template = models.ForeignKey('Template', null=True, blank=True, on_delete=models.CASCADE, related_name='reminder_mailinglist')

	send_reminder = models.BooleanField('Send events reminders', default=False)
	send_frequency = models.CharField('Send frequency', max_length=1, choices=SEND_FREQUENCY)

	def __str__(self):
		return self.name

	def get_messages(self, when=None):
		when = timezone.now() if when is None else when

		msgs = Message.objects.all()
		msgs = msgs.filter(mailing_lists=self)
		msgs = msgs.filter(
			(Q(publish_start=None) & Q(publish_end=None)) |
			(Q(publish_start__gte=when) & Q(publish_end=None)) |
			(Q(publish_start=None) & Q(publish_end__lte=when)) |
			(Q(publish_start__gte=when) & Q(publish_end__lte=when))
		)

		msgs = msgs.order_by('subject__order', 'subject__name', 'date', 'name')
		return msgs