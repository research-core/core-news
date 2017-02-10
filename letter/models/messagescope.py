from django.db import models

# Whether the message should be included in the internal, external or both newsletters
class MessageScope(models.Model):
	message_scope_id = models.AutoField('Id', primary_key=True)
	message_scope 	 = models.CharField(max_length=250)

	def __unicode__(self): return str(self.message_scope)