# -*- coding: utf-8 -*-


from iyoume.waybill import models as dr
from iyoume.room.views import show_known_user_main_room
from iyoume.tools.assistants import only_known_user
from django.shortcuts import render_to_response
from django.template import RequestContext


@only_known_user
def make_waybill(request):
    form = dr.WaybillMaker(request.POST or None)
    if form.is_valid():
        form.save(request)
        return show_known_user_main_room(request, u'Ваш маршрут зарегистрирован!')
    else:
        return render_to_response('add_way.html', {'form': form}, context_instance=RequestContext(request))


@only_known_user
def remove_waybill(request):
    form = dr.WaybillRemover(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return show_known_user_main_room(request, u'Ваш рейс отменён! Ваш рейтинг понижен.')   
    else:
        return render_to_response('base_form_middle.html', {'form': form}, context_instance=RequestContext(request))


@only_known_user
def search_waybill(request):
    form = dr.WaybillSearchEngine(request.POST or None)
    values = {'form': form}
    if form.is_valid():
        form.fill(values)
    return render_to_response('find_way.html', values, context_instance=RequestContext(request))


@only_known_user
def take_place(request):
    order_id = request.POST.get('order_id')
    if 'place_count' not in request.POST:
        request.POST = None
    try:
        form = dr.WaybillCash(order_id, request.POST or None)
        if form.is_valid():
            comment = dr.Waybill.objects.get(pk=order_id).comment
            form.post_form_comment = u'<h1>О рейсе</h1>{comment}'.format(comment=comment)
            form.save(request)
            return show_known_user_main_room(request, u'Ваш заказ учтён!') 
    except:
        return show_known_user_main_room(request, u'Рейс недоступен! Попробуте снова.')      
    values = {'form': form, 'order_id': order_id}
    return render_to_response('base_form.html', values, context_instance=RequestContext(request))


@only_known_user
def trips(request):
    """    
    """
    user_orders = dr.Passenger.objects.filter(user=request.user)
    values =  {'user_orders': user_orders}
    context = RequestContext(request)
    return render_to_response('trip.html', values, context_instance=context)


@only_known_user
def cancel_trip(request):
    """    
    """
    pk = request.POST.get('user_order_pk')
    try:
        user_order = dr.Passenger.objects.get(pk=pk)
        order = user_order.order
        order.place_count = order.place_count + user_order.place_count
        order.luggage_count = order.luggage_count + user_order.luggage_count
        order.save()
        user_order.delete()
    finally:
        return show_known_user_main_room(request, u'Ваш заказ аннулирован!') 


@only_known_user
def travel(request):
    """    
    """
    context = RequestContext(request)
    form = dr.TravelMaker(request.POST or None)
    if form.is_valid():
        travel = form.save(request)
        return render_to_response('travel.html', {'travel': travel}, context_instance=context)
    return render_to_response('base_form.html', {'form': form}, context_instance=context)
        

@only_known_user
def passangers(request):
    """    
    """
    orders = ((order, order.user_orders()) for order in dr.Waybill.objects.filter(driver=request.user))
    values = {'orders': orders}
    context = RequestContext(request)
    return render_to_response('passangers.html', values, context_instance=context)





