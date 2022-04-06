import datetime
import json
from uuid import UUID

import pytz
from celery import shared_task
from django.conf import settings
from django.db.models import Q
from django_celery_beat.models import PeriodicTask, MINUTES, IntervalSchedule

from .models import Mailing, Client
from .telegramm import TeleMessage


@shared_task(name='send_messages')
def send_messages(title, uuid):
    current_time = datetime.datetime.now(tz=getattr(pytz, settings.TIME_ZONE))
    mailing = Mailing.objects.get(uuid=UUID(uuid))
    task = PeriodicTask.objects.get(name=title)
    if mailing.ended > current_time > mailing.started:
        number = [x for x in mailing.filters if len(x) == 3 and x.isdigit()]
        tags = [x for x in mailing.filters if x not in number]
        clients = Client.objects.filter(Q(mobile_code__in=number) | Q(tag__name__in=tags))
        TeleMessage().send_message(json.dumps(list(clients.values())))
        task.enabled = False
        task.save()
    else:
        TeleMessage().send_message("Не время для сообщений!")
        task.interval = IntervalSchedule.objects.get(every=30, period=MINUTES)
