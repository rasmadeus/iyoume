# -*- coding: UTF-8 -*-


from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime 
from iyoume.tools.assistants import set_style
from iyoume.tools.google_geo import get_coords
from iyoume.tools.assistants import is_equals


class GeoPoint(models.Model):
    """    
    """
    lng = models.FloatField(verbose_name=u'Долгота пункта')
    lat = models.FloatField(verbose_name=u'Широта пункта')
    name = models.CharField(verbose_name=u'Название пункта', max_length=128)
    
    
    @staticmethod
    def make(coords):
        obj = GeoPoint()
        obj.lng = coords[0]
        obj.lat = coords[1]
        obj.name = coords[2]
        obj.save()
        return obj    
    
    
    def about_to(self, point):
        return is_equals(self.lng, point[0]) and is_equals(self.lat, point[1])
    
    
    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class Waybill(models.Model):
    """    
    """
    class Admin:
        list_display = ('driver') 


    def __unicode__(self):
        return u'Откуда: {from_point}; Куда: {to_point}; Когда: {date};'.format(\
            from_point=self.from_point.name,\
            to_point=self.to_point.name,\
            date=self.date\
        )
        
        
    def about_to(self, from_point, to_point):
        return self.from_point.about_to(from_point) and self.to_point.about_to(to_point)


    def user_orders(self):
        return Passenger.objects.filter(order=self)
    

    driver = models.ForeignKey(User)
    from_point = models.ForeignKey(GeoPoint, related_name='from_point')
    to_point = models.ForeignKey(GeoPoint, related_name='to_point')
    place_count = models.PositiveSmallIntegerField(verbose_name=u'Количество мест', default=4)
    luggage_count = models.PositiveSmallIntegerField(verbose_name=u'Мест для багажа', default=2)
    comment = models.TextField(verbose_name=u'Комментарий о месте встречи')
    date = models.DateTimeField()
    
    @staticmethod
    def remove_old_waybills():
        from django.utils import timezone
        for waybill in (waybill for waybill in Waybill.objects.all() if waybill.date<timezone.now()):
            for passenger in Passenger.objects.filter(order=waybill):
                passenger.delete()
            waybill.from_point.delete()
            waybill.to_point.delete()
            waybill.delete()
            
            
class Passenger(models.Model):
    """    
    """
    user = models.ForeignKey(User)
    order = models.ForeignKey(Waybill, related_name='order')    
    place_count = models.PositiveSmallIntegerField(verbose_name=u'Количество занятых мест', default=1)
    luggage_count = models.PositiveSmallIntegerField(verbose_name=u'Количество занятых мест для багажа', default=0)


class GeoPointField(forms.CharField):
    """    
    """
    default_error_messages = {
        'not_exist': 'Мы не нашли этот пункт. Локализуйте запрос.',
    }


    def clean(self, value): 
	super(GeoPointField, self).clean(value)
        try:   
            coords = get_coords(value)
            coords.append(value)
            return coords
        except:
            raise forms.ValidationError(self.default_error_messages['not_exist'])


class WaybillMaker(forms.Form):
    """    
    """
    processor = '/waybill/add/'
    submit_comment = u'Зарегистрировать рейс'
    
    from_point = GeoPointField(help_text=u'Пункт отправления', max_length=256)
    to_point = GeoPointField(help_text=u'Пункт назначения', max_length=256)
    place_count = forms.IntegerField(help_text=u'Количество мест', initial=4)
    luggage_count = forms.IntegerField(help_text=u'Количество багажных мест', initial=2)
    date = forms.DateTimeField(\
        help_text=u'Когда отправление', 
        required=False, input_formats=["%d.%m.%Y %H:%M:%S"],\
        initial=datetime.now()\
        )
    comment = forms.CharField(widget = forms.Textarea, help_text=u'Оставьте комментарий о месте встречи, транспорте.')
    
    
    def save(self, request):
        data = self.cleaned_data
        do = Waybill()
        do.driver = User.objects.get(pk=request.user.pk)
        do.from_point = GeoPoint.make(data['from_point'])
        do.to_point = GeoPoint.make(data['to_point'])
        do.place_count = data['place_count']
        do.luggage_count = data['luggage_count']
        do.date = data['date']
        do.comment = data['comment']
        do.save()
    
    
    set_style(from_point, u'Пункт сбора, укажите улицу')
    set_style(to_point, u'Куда едем?')
    set_style(place_count, u'Сколько берём пассажиров?')
    set_style(luggage_count, u'Сколько багажных мест?')
    set_style(date, u'Дата и время отправления')
    set_style(comment, 
        u'Опишите подробнее место встречи и ваш транспорт,\
        пожелания к пассажирам. Например: хороший жигуль, домчит быстро.\
        Здесь же можно оставить дополнительную информацию о месте встречи.'\
    )


class WaybillRemover(forms.Form):
    """    
    """
    processor = '/waybill/del/'
    submit_comment = u'Отменить выбранные рейсы'
    page_title = u'Редактирование списка рейсов'
    header = u'Мои предложения для пассажиров'

    orders = forms.ModelMultipleChoiceField(queryset=Waybill.objects.none())
    set_style(orders, u'Ваши предложения по рейсам')
    
    def __init__(self, user, *args, **kwargs):
        super(WaybillRemover, self).__init__(*args, **kwargs)
        self.fields['orders'].queryset = Waybill.objects.filter(driver=user)
        
    def save(self):
        from tools.assistants import send_sms
        from iyoume_user import models as iy
        data = self.cleaned_data
        for order in data['orders']:
            user_orders = Passenger.objects.filter(order=order)
            for user_order in user_orders:
                iyoume_user = iy.IyoumeUser.objects.get(user=user_order.user)
                text = u'Рейс {from_point} - {to_point} {date} был отменён водителем.'
                from_point = order.from_point.name
                to_point = order.to_point.name
                date = order.date
                send_sms(\
                    iyoume_user.phone_number,\
                    text.format(\
                        from_point=from_point,\
                        to_point=to_point,\
                        date=date\
                    )\
                )
                user_order.delete()
            order.to_point.delete()
            order.from_point.delete()
            order.delete()        
        
        
from tools.google_geo import get_coords 
        
        
class WaybillSearchEngine(forms.Form):
    """    
    """
    processor = '/waybill/find/'
    submit_comment = u'Найти машину'
    page_title = u'Искать маршрут'    
    
    from_point = forms.CharField(help_text=u'Пункт отправления', max_length=256)
    to_point = forms.CharField(help_text=u'Пункт назначения', max_length=256)
    
    set_style(from_point, u'Откуда едем?')
    set_style(to_point, u'Куда едем?')
    
    
    def fill(self, values):
        data = self.cleaned_data
        from_point = get_coords(data['from_point'])
        to_point = get_coords(data['to_point'])
        orders = [order for order in Waybill.objects.all() if order.about_to(from_point, to_point)]
        values['orders'] = orders
    
    
class WaybillCash(forms.Form):
    """    
    """
    error_messages = {
        'place_count': u'На этом рейсе свободно мест: {place_count}',
        'luggage_count': u'На этом рейсе можно взять багажа: {luggage_count}'
    }
    
    processor = '/waybill/take/'
    submit_comment = u'Занять место'
    page_title = u'Занять место'
    header = u'Занять место'
    
    place_count = forms.IntegerField(min_value=1, help_text=u'Сколько мест занять?', initial=1)
    luggage_count = forms.IntegerField(min_value=0, help_text=u'У вас есть багаж, который не уместится в салоне?', initial=0)
          
    set_style(place_count, u'Сколько вы хотите занять мест?')
    set_style(luggage_count, u'Сколько у вас багажа?')
  
  
    def __init__(self, order_id, *args, **kwargs):
        super(WaybillCash, self).__init__(*args, **kwargs)
        self._order = Waybill.objects.get(pk=order_id)
        
        
    def clean_place_count(self):
        place_count = self.cleaned_data['place_count']
        if place_count > self._order.place_count:
            raise forms.ValidationError(self.error_messages['place_count'].format(place_count=self._order.place_count))
        else:
            return place_count
        
        
    def clean_luggage_count(self):
        luggage_count = self.cleaned_data['luggage_count']
        if luggage_count > self._order.luggage_count:
            raise forms.ValidationError(self.error_messages['luggage_count'].format(luggage_count=self._order.luggage_count))
        else:
            return luggage_count
        
        
    def save(self, request):
        data = self.cleaned_data
        place_count = data['place_count']
        luggage_count = data['luggage_count']
        user_order = Passenger()
        user_order.order = self._order
        user_order.user = request.user
        user_order.place_count = place_count
        user_order.luggage_count = luggage_count
        self._order.place_count = self._order.place_count - place_count
        self._order.luggage_count = self._order.luggage_count - luggage_count
        self._order.save()
        user_order.save()


class Travel(models.Model):
    """
    """
    passangers = models.ManyToManyField(User)
    from_point = models.ForeignKey(GeoPoint, related_name='travel_from_point')
    to_point = models.ForeignKey(GeoPoint, related_name='travel_to_point')
    meeting_point = models.TextField(verbose_name=u'Комментарий о месте встречи')


    def about_to(self, from_point, to_point):
        return self.from_point.about_to(from_point) and self.to_point.about_to(to_point)
    
    
    @staticmethod
    def find(from_point, to_point):
        return [travel for travel in Travel.objects.all() if travel.about_to(from_point, to_point)]


class TravelMaker(forms.Form):
    processor = '/waybill/travel/'
    submit_comment = u'Искать попутчиков'
    header = u'Поиск попутчиков'
    
    
    from_point = GeoPointField(help_text=u'Откуда едите', max_length=256)
    to_point = GeoPointField(help_text=u'Куда едите', max_length=256)
    comment = forms.CharField(widget = forms.Textarea, help_text=u'Оставьте комментарий о месте встречи')

    
    def __unicode__(self):
        return u'{from_point} -> {to_point}'.format(from_point=self.from_point, to_point=self.to_point)

    
    def save(self, request):
        data = self.cleaned_data
        from_point = data['from_point']
        to_point = data['to_point']
        travels = Travel.find(from_point, to_point)
        if len(travels) == 0:
            travel = Travel()
            travel.from_point = GeoPoint.make(from_point)
            travel.to_point = GeoPoint.make(to_point)
            travel.meeting_point = data['comment']
            travel.save()
            travel.passangers.add(request.user)
        else:
            travel = travels[0]
            if request.user not in travel.passangers.all():
                travel.passangers.add(request.user)
        return travel


    set_style(from_point, u'Пункт отправления')
    set_style(to_point, u'Пункт назначения')
    set_style(comment, u'Опишите место встречи. Если ваш заказ первый, то все попутчики будут собираться в этом месте.')