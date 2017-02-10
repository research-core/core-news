# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

@login_required
def user_profile(request):
	return render_to_response('neuroauth/userprofile.html', {}, context_instance=RequestContext(request))
