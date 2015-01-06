# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
import hashlib
from iyoume.tools.assistants import set_style


class IyoumeUserRegInfo(models.Model):
    def fill_code(self):
	import random
	code = str(random.randint(10000, 1000000))
	self.code = hashlib.md5(code).hexdigest()
	self.is_waiting_sms = True
	return code

    def check_sms(self, code):
	if self.is_waiting_sms == False:
		return False
	self.is_waiting_sms = False
	self.is_accepted = self.code == hashlib.md5(code).hexdigest() 		
        self.code = ''
	self.save()
	return self.is_accepted


    user = models.ForeignKey(User, unique=True)
    code = models.CharField(max_length=256, default='')
    is_waiting_sms = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)	


    def __unicode__(self):
        return u'{0}'.format(self.user.username)


class IyoumeUser(models.Model):
    user = models.ForeignKey(User, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)


    def __unicode__(self): 
       	return u'{0}'.format(self.user.username)


from django import forms
from tools.assistants import is_phone_number


class PhoneNumberField(forms.CharField):
    def __init__(self, **kwargs):
	forms.CharField.__init__(self, **kwargs)
	self._exist_mode = False


    default_error_messages = {
        'is_not_number': 'Просто введите 10 цифр без 8 и +7',
	'exist_phone': 'Такой номер телефона уже зарегистрирован',
	'not_exist_phone': 'Такой номер не зарегистрирован',
    }


    def check_exist_number(self):
	self._exist_mode = True


    def check_not_exist_number(self):
	self._exist_mode = False


    def clean(self, value):
        super(PhoneNumberField, self).clean(value)
	if not is_phone_number(value):
            raise forms.ValidationError(self.error_messages['is_not_number'])
	contain = len(IyoumeUser.objects.filter(phone_number=value)) != 0
	if not self._exist_mode and contain:
            raise forms.ValidationError(self.error_messages['exist_phone'])
	if  self._exist_mode and not contain:
            raise forms.ValidationError(self.error_messages['not_exist_phone'])
	return value


class NameField(forms.CharField):
    default_error_messages = {
       	'exist_username': 'Пользователь с таким именем уже существует.',
    }


    def clean(self, value):
	super(NameField, self).clean(value)
	if len(User.objects.filter(username=value)) != 0:
            raise forms.ValidationError(self.error_messages['exist_username'])
        else:
            return value


from tools.assistants import send_sms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect


class IyoumeUserMaker(forms.Form):
    page_title = u'Регистрация нового пользователя iyoume'
    header = u'Сейчас мы быстренько оформим вам пропуск'
    processor = u'/user/'
    check_box_comment = u'Я принимаю условия <a href="/room/license/" target="_blank">лицензионного соглашения</a>'
    submit_comment = u'Обработать данные'	
    post_form_comment = u'<a href="/user/restore_password/">Забыли пароль?</a>'
        
        
    username = NameField(help_text=u'Какое имя записать в пропуск?', max_length = 30)
    password = forms.CharField(help_text=u'Ваш пароль никому неизвестен?', widget = forms.PasswordInput, min_length = 8, max_length = 30)
    phone_number = PhoneNumberField(help_text=u'Скажите, пожалуста, ваш номер телефона?', max_length=10)
    user_accept_license = forms.BooleanField()


    set_style(username, u'Ваш псевдоним на сайте')
    set_style(password, u'Ваш пароль на сайте')
    set_style(phone_number, u'Номер вашего телефона')
    
    
    def save(self, request):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['username'], password=data['password'])
        iyoumeUser = IyoumeUser.objects.create(user=user, phone_number=data['phone_number'])
        iyoumeUser.save()	
        userRegInfo = IyoumeUserRegInfo.objects.create(user=user)
        code = userRegInfo.fill_code()
        userRegInfo.save()
        send_sms(data['phone_number'], code)
        return render_to_response('base_form.html', {'form': NewUserChecker(), 'user_id': user.id}, context_instance=RequestContext(request))


class UserData:
    def __init__(self, request):
	self.user_id = int(request.POST.get('user_id'))
	self.user = User.objects.get(pk=self.user_id)
	self.user_reg_info = IyoumeUserRegInfo.objects.get(user=self.user)
	self.iyoume_user = IyoumeUser.objects.get(user=self.user)


    def delete(self):
        self.user.delete()

        
    def check_sms(self, code):
	return self.user_reg_info.check_sms(code)
    

class NewUserChecker(forms.Form):
    page_title = u'Проверка введённых данных'
    header = u'Ждите, вам идёт смска'
    processor = u'/user/check_new_user/'
    submit_comment = u'Обработать данные'


    code = forms.CharField(help_text=u'Введите сообщение, которое мы вам выслали')


    set_style(code, u'Ждите, вам идёт смска')
    
    
    def save(self, request):
        try:
            user_data = UserData(request)
            if user_data.user_reg_info.check_sms(self.cleaned_data['code']):
                return redirect('/user/login/')
            else:
                user_data.delete()
                return redirect('/room/bad_status/')
        except:
            return redirect('/room/bad_status/')


from django.contrib import auth


class Login(forms.Form):
	def to_error_page(self):
            self.header = u'Охраннику не понравился ваш пропуск, попробуйте ещё раз'


	page_title = u'Вход в систему iyoume'
	header = u'Предъявите пропуск, пожалуйста'
	processor = u'/user/login/'
	submit_comment = u'Вот мой пропуск'
        post_form_comment = u'<a href="/user/restore_password/">Забыли пароль?</a>'
        
        
	name_or_phone = forms.CharField(help_text=u'Стой! Кто идёт?', max_length=256)
	password = forms.CharField(help_text=u'А ну говори пароль', widget = forms.PasswordInput, max_length = 30)


	set_style(name_or_phone, u'Ваш логин или номер телефона')
	set_style(password, u'Введите ваш пароль')
        
        
        def find_user_by_phone(self, name_or_phone, password):
            iyoume_users = IyoumeUser.objects.filter(phone_number=name_or_phone)
            if len(iyoume_users) != 0:
                iyoume_user = iyoume_users[0]
                return auth.authenticate(username=iyoume_user.user.username, password=password)
            return None
        
        
        def try_auth_user(self, request):
            data = self.cleaned_data
            name_or_phone = data['name_or_phone']
            password = data['password']
            user = auth.authenticate(username=name_or_phone, password=password)
            if user is None:
                user = self.find_user_by_phone(name_or_phone, password)
            if user is not None and user.is_active:
                iyoume_user_reg_info = IyoumeUserRegInfo.objects.get(user=user)
                if iyoume_user_reg_info.is_accepted: 
                    auth.login(request, user)
                    return True
            self.to_error_page()
            return False


class UserPasswordRestorer(forms.Form):
	def to_error_page(self):
            self.header = u'Неправильный код, попробуёте сново'


	page_title = u'Восстановление утерянного пропуска'
	header = u'Потеряли пропуск? Ничего страшного'
	processor = u'/user/restore_password/'
	submit_comment = u'Прошу восстановить мой пропуск'


	phone_number = PhoneNumberField(help_text=u'Телефон, указанный при регистрации', max_length=10)
	phone_number.check_exist_number()


	set_style(phone_number, u'Номер вашего телефона')
        
        
        def save(self, request):
            phone_number=self.cleaned_data['phone_number']
            iyoumeUser = IyoumeUser.objects.get(phone_number=phone_number)
            userRegInfo = IyoumeUserRegInfo.objects.get(user=iyoumeUser.user)
            code = userRegInfo.fill_code()
            userRegInfo.save()
            send_sms(phone_number, code)
            return render_to_response('base_form.html', {'form': RestoredUserChecker(), 'user_id': iyoumeUser.user.id}, context_instance=RequestContext(request))


class RestoredUserChecker(NewUserChecker):
	page_title = u'Восстановление пропуска пользователя'
	header = u'Приступим к восстановлению пропуска'
	processor = u'/user/check_restore_user/'
	submit_comment = u'Теперь это мой новый пароль'
        
        
	password = forms.CharField(help_text=u'Ваш новый пароль', widget = forms.PasswordInput, max_length = 30)


	set_style(password, u'Ваш новый пароль')
	

        def save(self, request):
            try:
                data = self.cleaned_data
                code = data['code']
                user_data = UserData(request)
                if user_data.check_sms(code):
                    user_data.user.set_password(data['password'])
                    user_data.user.save()
                    return redirect('/user/login/')
                else:
                    return redirect('/room/bad_status/')
            except:
                form = UserPasswordRestorer()
                form.to_error_page()
                return render_to_response('base_form.html', {'form': form}, context_instance=RequestContext(request))