from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
import pytz


class Mailing(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Начало рассылки')
    message = models.CharField(max_length=256)
    filters = models.CharField(max_length=64)
    ended = models.DateTimeField(verbose_name='Окончание рассылки')


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    number = PhoneNumberField()
    mobile_code = models.PositiveIntegerField(verbose_name='Код мобильного оператора')
    tags = TaggableManager()
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Message(models.Model):
    STATUSES = (
        ('Complete', 'Complete'),
        ('In process', 'In process'),
        ('Error', 'Error')
    )

    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUSES)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True)
    client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True)
