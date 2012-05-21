from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django import forms
from fetch.script import *
from fetch.mineWebservice import postRequest, alreadyRequested, getStudyList
from datetime import datetime
import thread

from pymongo import Connection

HOST = '127.0.0.1'
PORT = 27017
connection = Connection(HOST, PORT)

class ContactForm(forms.Form):
    email = forms.EmailField()
    gsid = forms.CharField()

@csrf_protect
def home(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            #if new request
            if not alreadyRequested(form.cleaned_data['gsid']):
                #save request data, download data, upload to server and thank you page
                postRequest(form.cleaned_data['gsid'], form.cleaned_data['email'])
                thread.start_new_thread(main,(form.cleaned_data['gsid'], None))
                return HttpResponse("Thanks for using M.I.N.E.") # Redirect after POST
            else:
                #request already posted page
                return HttpResponse("That study has already been requested")
    #if not post request make form to store input
    form = ContactForm() # An unbound form

    t = loader.get_template('studies/main.html')
    c = RequestContext(request, {'form':form,})
    return HttpResponse(t.render(c))

def data(request, studynumber):
    t = loader.get_template('studies/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def list(request):

    studylist = getStudyList()
    t = loader.get_template('studies/list.html')
    c = RequestContext(request, {'studylist':studylist,})
    return HttpResponse(t.render(c))


    

