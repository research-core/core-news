
from django.template    import RequestContext
from datetime           import *
from django.conf        import settings
from django.core.mail   import EmailMessage
from django.db          import connection
from django.db          import transaction
from django.http        import HttpResponse
from django.shortcuts   import render_to_response
from django.template.loader import render_to_string
from django.utils.encoding  import smart_str
from email.mime.text    	import MIMEText
from letter.models      	import Newsletter, Subject, Message


#**************************************************************************************
# Selects the messages to build the external/internal newsletter according to the
# 'isExternal' parameter is set to True or False, respectively
#**************************************************************************************
def __select_messages(isExternal, year=None, month=None, day=None):

	try:
		now = datetime.now()
		if not (month or day or year):
			year = now.year
			month = now.month
			day = now.day

		year = int(year)
		month = int(month)
		day = int(day)

		if isExternal:
			query = """ select letter_message.subject_id, subject_title, message_title,
						DATE_FORMAT(message_datetime ,%s),
						message_location,
						REPLACE(message_text, '\n' , '<br/>'), message_img, message_id, message_pubstart, message_pubend,
						newsletter_start_vpdt_id, newsletter_end_vpdt_id
						from letter_message inner join letter_subject on letter_message.subject_id = letter_subject.subject_id
						where (message_pubstart <= DATE('%s-%s-%s') or (message_pubstart is null)) and (message_pubend >= DATE('%s-%s-%s') or (message_pubend is null)) and ((message_scope_id = 2) or (message_scope_id = 3))
						order by letter_subject.subject_order, letter_subject.subject_title,
						letter_message.message_order, letter_message.message_datetime, letter_message.message_title """
		else:
			query = """ select letter_message.subject_id, subject_title, message_title,
						DATE_FORMAT(message_datetime ,%s),
						message_location,
						REPLACE(message_text, '\n' , '<br/>'), message_img, message_id, message_pubstart, message_pubend,
						newsletter_start_vpdt_id, newsletter_end_vpdt_id
						from letter_message inner join letter_subject on letter_message.subject_id = letter_subject.subject_id
						where (message_pubstart <= DATE('%s-%s-%s') or (message_pubstart is null)) and (message_pubend >= DATE('%s-%s-%s') or (message_pubend is null)) and ((message_scope_id = 1) or (message_scope_id = 3))
						order by letter_subject.subject_order, letter_subject.subject_title,
						letter_message.message_order, letter_message.message_datetime, letter_message.message_title """

		cursor = connection.cursor()
		# Monday, 7 November 2011, 12:00
		cursor.execute(query, ['%W, %e %M %Y, %H:%i', year, month, day, year, month, day])
		rows = cursor.fetchall()

		if( rows.__len__()==0 ):
			return None

		#Organize messages in subjects
		subjects = []
		messages = []
		last_subject = rows[0][0]
		for row in rows:
			if last_subject != row[0]:
				last_subject = row[0]
				subjects.append(messages)
				messages = []
			messages.append(row)
			
		subjects.append(messages)

		return subjects
	except ValueError:        
		return None


#**************************************************************************************
#Select event messages
#**************************************************************************************
def select_event_messages(year=None, month=None, day=None):

	try:
		now = datetime.now()
		if not (month or day or year):
			year = now.year
			month = now.month
			day = now.day

		year = int(year)
		month = int(month)
		day = int(day)

		query = """ select letter_message.subject_id, subject_title, message_title,
					DATE_FORMAT(message_datetime ,%s),
					message_location,
					REPLACE(message_text, '\n' , '<br/>'), message_img, message_id, message_pubstart, message_pubend,
					if( date(letter_message.message_datetime) = date('%s-%s-%s') , 1, 0 )
					from letter_message inner join letter_subject on letter_message.subject_id = letter_subject.subject_id
					where letter_message.message_event=true and
					letter_message.message_datetime is not null and
					DATE_SUB(date(letter_message.message_datetime), INTERVAL 1 DAY) <= date('%s-%s-%s') and
					date('%s-%s-%s') <= date(letter_message.message_datetime)
					order by letter_subject.subject_order, letter_subject.subject_title,
					letter_message.message_order, letter_message.message_datetime, letter_message.message_title """

		cursor = connection.cursor()
		cursor.execute(query, ['%W, %b %d, %Y at %H:%i', year, month, day, year, month, day, year, month, day])
		rows = cursor.fetchall()

		if( rows.__len__()==0 ):
			return None
		
		return rows
	except ValueError:
		return None

#**************************************************************************************
# Build the external/internal newsletter html according to the
# 'isExternal' parameter is set to True or False, respectively
#**************************************************************************************
def __build_newsletter(isExternal, year=None, month=None, day=None):
	try:
		now = datetime.now()
		#if the variables month, day and year are not defined, it will set them with the current day
		if not (month or day or year):
			year = now.year
			month = now.month
			day = now.day
		year = int(year)
		month = int(month)
		day = int(day)

		subjects = __select_messages(isExternal, year, month, day)

		if subjects:
			processed_date = datetime(year, month, day)
			title = 'CNP News - %s' % processed_date.strftime("%b %d, %Y");
			
			news = Newsletter(
				newsletter_title=title,
				newsletter_html='',
				newsletter_built=now,
				newsletter_active=True,
				newsletter_sendfrom = 'newsletter',
				newsletter_external = isExternal
			)
			news.save();
			#if there are messages to send, build the newsletter html

			#update the messages publish dates in case of null
			for sub in subjects:
				for msg in sub:
					msgModel = Message.objects.get(message_id=msg[7])
					if( msg[8] == None ):
						msgModel.message_pubstart = processed_date
						msgModel.newsletter_start_vpdt = news #save the id of the newsletter where the date was updated
					if( msg[9] == None ):
						msgModel.message_pubend = processed_date
						msgModel.newsletter_end_vpdt = news #save the id of the newsletter where the date was updated
					
					msgModel.save()
			#end
			
			if not news.newsletter_datetime:
				news.newsletter_datetime = datetime(year, month, day)

			html = render_to_string('letter/email.html', {'subjects': subjects, 'title': title, 'SITE_URL': settings.SITE_URL})
			
			news.newsletter_html = html
			news.save()
			return (True, 'Built with success')
		else:
			return (True, 'No messages to build')

	except ValueError:
		return (False, 'Error %s' % ValueError)


#**************************************************************************************
#View to build the newsletter html - wrapper for backwards compatibility
#**************************************************************************************
def build_newsletter(request, year=None, month=None, day=None):

	ret = []

	# Build the internal newsletter
	res_val, res_msg = __build_newsletter(False, year=None, month=None, day=None)
	if not res_val:
		return HttpResponse('Error %s' % res_msg)
	ret.append(res_msg)

	# Build the external newsletter
	res_val, res_msg = __build_newsletter(True, year=None, month=None, day=None)
	if not res_val:
		return HttpResponse('Error %s' % res_msg)
	ret.append(res_msg)

	return HttpResponse('Internal Newsletter: %s<br>External Newsletter: %s<br>' % (ret[0], ret[1]))



#**************************************************************************************
#View to build the events html
#**************************************************************************************
#def build_event(request, sdate=None):
#
#        if( sdate == None ):
#            date = datetime.now()
#        else:
#            date = datetime.strptime( sdate, "%Y%m%d" )
def build_event(request, year=None, month=None, day=None):

	try:
		now = datetime.now()
		#if the variables month, day and year are not defined, it will set them with the current day
		if not (month or day or year):
			year = now.year
			month = now.month
			day = now.day

		year = int(year)
		month = int(month)
		day = int(day)
		
		messages = select_event_messages(year, month, day)
			
		if messages:
			processed_date = datetime(year, month, day)
			
			for message in messages:
				if(message[10]==1):
					when = 'Today'
				else:
					when = 'Tomorrow'

				title = "%s: %s - %s" % (when, message[1], message[2])
				html = render_to_string('letter/event.html', {'when': when.upper(), 'message': message, 'subject': message[1], 'title': message[2], 'SITE_URL': settings.SITE_URL})
				news = Newsletter(
					newsletter_title=title,
					newsletter_html=html,
					newsletter_built=now,
					newsletter_active=True,
					newsletter_datetime = processed_date,
					newsletter_sendfrom = 'events'
				)
				news.save()
			return HttpResponse('Built with success')
		else:
			return HttpResponse('No messages to build')

	except ValueError:
		return HttpResponse('Error %s' % ValueError)


#**************************************************************************************
#Send messages built messages
#**************************************************************************************
def send_newsletter(request, id=None, year=None, month=None, day=None):
	try:
		now = datetime.now()

		#Choose the message to send. You can choose it by ID, or by date. If none of the variables are set it will choose the last built message
		if id:
			new = Newsletter.objects.get(newsletter_id=id)
		elif month and day and year:
			newsletters = Newsletter.objects.filter(newsletter_built__year=year, newsletter_built__month=month, newsletter_built__day=day).filter(newsletter_active=True)
			if newsletters.count() > 0:
				new = newsletters[0]
			else:
				return HttpResponse('No newsletter on this date: Month %s - Day %s - Year %s' % (month, day, year))
		else:
			newsletters = Newsletter.objects.filter(newsletter_active=True).filter(newsletter_sent__isnull=True).order_by('-newsletter_id')

		#if there isn't any message to send don't do nothing
		if newsletters.count() > 0:
			for new in newsletters:
				msg = MIMEText(smart_str(new.newsletter_html), 'html')
				
				settings.EMAIL_HOST_NAME = settings.EMAIL_DATA[new.newsletter_sendfrom]['host_name']
				settings.EMAIL_HOST_USER = settings.EMAIL_DATA[new.newsletter_sendfrom]['host_user']
				settings.EMAIL_HOST_PASSWORD = settings.EMAIL_DATA[new.newsletter_sendfrom]['host_password']

				msg['Subject'] = new.newsletter_title
				msg['From'] = "%s <%s>" %(settings.EMAIL_HOST_NAME, settings.EMAIL_HOST_USER)
				if(new.newsletter_external): msg['To'] = settings.EMAIL_TO_EXTERNAL
				else: msg['To'] = settings.EMAIL_TO
				email = EmailMessage(msg['Subject'], new.newsletter_html, from_email=msg['From'], to=msg['To'])
				email.content_subtype = "html"
				email.send()
				new.newsletter_sent = now
				new.newsletter_active = True
				new.save()
				
			return HttpResponse('Sent with success')
		else:
			return HttpResponse('Nothing to send')
	except ValueError:

		return HttpResponse('Error %s' % ValueError)


#**************************************************************************************
# Displays a newsletter in the browser
#**************************************************************************************
def show_newsletter(request, scope, id=None, year=None, month=None, day=None):
	if not request.user.is_authenticated():
		return HttpResponse('You need to login')

	if id:
		if scope == 'int': new = Newsletter.objects.get(newsletter_id=id, newsletter_external=False)
		elif scope == 'ext': new = Newsletter.objects.get(newsletter_id=id, newsletter_external=True)
	elif month and day and year:
		if scope == 'int': newsletters = Newsletter.objects.filter(newsletter_datetime__year=year, newsletter_datetime__month=month, newsletter_datetime__day=day, newsletter_external=False)
		elif scope == 'ext': newsletters = Newsletter.objects.filter(newsletter_datetime__year=year, newsletter_datetime__month=month, newsletter_datetime__day=day, newsletter_external=True)
		
		if newsletters.count() > 0:
			new = newsletters[0]
		else:
			return HttpResponse('No newsletter on this date: Month %s - Day %s - Year %s' % (month, day, year))
	else:
		if scope == 'int': new = Newsletter.objects.filter(newsletter_active=True, newsletter_external=False).order_by('-newsletter_id')[0]
		elif scope == 'ext': new = Newsletter.objects.filter(newsletter_active=True, newsletter_external=True).order_by('-newsletter_id')[0]
		

	return HttpResponse(new.newsletter_html)


#**************************************************************************************
# Displays a draft of a newsletter
# For test
#**************************************************************************************
def test_newsletter(request, scope, year=None, month=None, day=None):
	if not request.user.is_authenticated():
		return HttpResponse('You need to login')

	try:
		now = datetime.now()
		if not (month or day or year):
			year = now.year
			month = now.month
			day = now.day

		year = int(year)
		month = int(month)
		day = int(day)

		if scope == 'int': subjects = __select_messages(False, year, month, day)
		elif scope == 'ext': subjects = __select_messages(True, year, month, day)

		if subjects:
			processed_date = datetime(year, month, day)
			title = 'CNP News - %s' % processed_date.strftime("%b %d, %Y");
			html = render_to_string('letter/email.html', {'subjects': subjects, 'title': title, 'SITE_URL': settings.SITE_URL})

			return HttpResponse(html)
		else:
			return HttpResponse('No messages to build')

	except ValueError:
		return HttpResponse('Error %s' % ValueError)


#**************************************************************************************
# Displays a draft of tomorrow
# For test
#**************************************************************************************
def test_event(request, year=None, month=None, day=None):
	if not request.user.is_authenticated():
		return HttpResponse('You need to login')

	try:
		now = datetime.now()
		if not (month or day or year):
			year  = now.year
			month = now.month
			day   = now.day

		year = int(year)
		month = int(month)
		day = int(day)

		messages = select_event_messages(year, month, day)

		if messages:
			processed_date = datetime(year, month, day)
			html = ''
			for message in messages:

				if(message[10]==1):
					when = 'Today'
				else:
					when = 'Tomorrow'
					
				title = "%s: %s - %s" % (when, message[1], message[2])
				html += render_to_string('letter/event.html', {'when': when.upper(),'message': message, 'subject': message[1], 'title': message[2], 'SITE_URL': settings.SITE_URL})
				
			return HttpResponse(html)
		else:
			return HttpResponse('No messages to build')

	except ValueError:
		return HttpResponse('Error %s' % ValueError)