from django.template import RequestContext
from django.shortcuts import render_to_response

def show_known_user_main_room(request, header_main):
    template = 'main_known_user.html'
    values =  {'header_main': header_main}
    context = RequestContext(request)	
    return render_to_response(template, values, context_instance=context)

def build_main_room(request):
  template_name = 'main_known_user.html' if request.user.is_authenticated() else 'main_unknown_user.html'
  return render_to_response(template_name, context_instance=RequestContext(request))

from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from iyoume.room import models as room
class RoomView(DetailView):
    model = room.Room
    context_object_name = 'room'

    def get_object(self):
        return get_object_or_404(room.Room, slug__iexact=self.kwargs['slug'])
