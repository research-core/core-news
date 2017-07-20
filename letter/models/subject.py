from django.db import models

class Subject(models.Model):
	subject_id 		= models.AutoField('Id', primary_key=True)
	subject_title 	= models.CharField(max_length=200)
	subject_text 	= models.TextField('Text', blank=True, null=True,)
	subject_active 	= models.NullBooleanField('Active')
	subject_order 	= models.IntegerField('Order')
	
	def __unicode__(self): return self.subject_title