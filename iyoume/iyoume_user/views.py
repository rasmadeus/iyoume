# -*- coding: utf-8 -*-


from django.shortcuts import redirect
from django.shortcuts import render_to_response
from iyoume.iyoume_user import models as iu
from django.template import RequestContext
	
                
def check_user(request):
    form = iu.NewUserChecker(request.POST or None)
    if form.is_valid():
        return form.save(request)
    else:
        values = {'form': form, 'user_id': request.POST.get('user_id')}
        return render_to_response('base_form.html', values, context_instance=RequestContext(request))


def login(request):
    form = iu.Login(request.POST or None)
    if form.is_valid():
        if form.try_auth_user(request):
            return redirect('/')        
    return render_to_response('base_form.html', {'form': form}, context_instance=RequestContext(request))
    

def add_new_user(request):
    form = iu.IyoumeUserMaker(request.POST or None)
    if form.is_valid():
        return form.save(request)
    else:
        return render_to_response('base_form.html', {'form': form}, context_instance=RequestContext(request))
        
        
def restore_password(request):
    form = iu.UserPasswordRestorer(request.POST or None)
    if form.is_valid():
        return form.save(request)
    else:
        return render_to_response('base_form.html', {'form': form}, context_instance=RequestContext(request))


def try_restore_user(request):
    form = iu.RestoredUserChecker(request.POST or None)
    if form.is_valid():
        return form.save(request)
    else:
        return render_to_response('base_form.html', {'form': form, 'user_id': request.POST.get('user_id')}, context_instance=RequestContext(request))
   
    
def registration_room(request):
    if request.user.is_authenticated():
        return render_to_response('registration_known_user.html', context_instance=RequestContext(request))
    return add_new_user(request)




