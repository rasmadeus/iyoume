# -*- coding: utf-8 -*-


from django.db import models


class Room(models.Model):
	slug = models.SlugField(primary_key=True, max_length=250, unique=True)
	header = models.CharField(max_length=100)
	content = models.TextField()


  	def get_absolute_url(self):
    		return '/{0}/'.format(self.slug)


	def __unicode__(self):
        	return u'{0}'.format(self.slug)

