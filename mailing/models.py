import pytz
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager


class Mailing(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Начало рассылки')
    message = models.CharField(max_length=256)
    filters = models.CharField(max_length=64, blank=True)
    ended = models.DateTimeField(verbose_name='Окончание рассылки')

    def __str__(self):
        return self.message


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    number = PhoneNumberField()
    mobile_code = models.CharField(verbose_name='Код мобильного оператора', editable=False, max_length=3)
    tags = TaggableManager(blank=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.mobile_code = ''.join([x for x in self.number.raw_input if x.isdigit()][1:4])
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.number}'


class Message(models.Model):
    STATUSES = (
        ('Complete', 'Complete'),
        ('In process', 'In process'),
        ('Error', 'Error')
    )

    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUSES)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True, related_name='dispatch')
    client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.client} - {self.mailing}'
