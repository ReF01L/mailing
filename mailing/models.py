import json
from uuid import uuid4

import pytz
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule, SECONDS
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager


class Mailing(models.Model):
    started = models.DateTimeField(verbose_name='Начало рассылки')
    message = models.CharField(max_length=256)
    filters = ArrayField(models.CharField(max_length=64), blank=True)
    ended = models.DateTimeField(verbose_name='Окончание рассылки')
    uuid = models.UUIDField(editable=False, unique=True, blank=True)

    def get_title(self):
        return self.message if len(self.message) < 10 else self.message[:10]

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid4()
        title = f'{self.get_title()} - {self.uuid}'
        PeriodicTask.objects.filter(name=title).delete()
        PeriodicTask.objects.create(
            name=f'{self.get_title()} - {self.uuid}',
            task='send_messages',
            args=json.dumps([title, self.uuid.hex]),
            start_time=self.started,
            interval=IntervalSchedule.objects.get(every=10, period=SECONDS),
            one_off=True
        )

        super(Mailing, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        PeriodicTask.objects.filter(name=f'{self.get_title()} - {self.pk}').delete()
        super(Mailing, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.message}'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    number = PhoneNumberField()
    mobile_code = models.CharField(verbose_name='Код мобильного оператора', editable=False, max_length=3)
    tag = TaggableManager(blank=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.mobile_code = ''.join([x for x in self.number.raw_input if x.isdigit()][1:4])
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.number}'


class Message(models.Model):
    STATUSES = (
        ('Complete', 'Complete'),
        ('InProcess', 'In Process'),
        ('Error', 'Error')
    )

    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUSES)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True, related_name='dispatch')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.client} - {self.mailing}'
