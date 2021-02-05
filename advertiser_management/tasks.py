from celery import Celery, task
from django.db.models import Count
from django.db.models.functions import TruncHour, TruncDay
from .models import View, Click, ReportDaily, ReportHourly, Ad
from datetime import datetime

@task(name='report_hourly')
def save_hourly():
    clicks = Click.objects.annotate(date=TruncHour('time')).values('date', 'ad_id') \
        .annotate(count=Count('ad_id')).values('ad_id', 'date', 'count').filter(time__hour=datetime.now().hour)
    views = View.objects.annotate(date=TruncHour('time')).values('date', 'ad_id') \
        .annotate(count=Count('ad_id')).values('ad_id', 'date', 'count').filter(time__hour=datetime.now().hour)
    report = ReportHourly.objects
    for ad in Ad.objects.values_list('pk'):
        report.create(ad_id=ad, clicks=clicks.get(ad_id=ad, default=0), time=datetime.now(), views=views.get(ad_id=ad),
                      default=0)


@task(name='report_daily')
def save_daily():
    clicks = Click.objects.annotate(date=TruncDay('time')).values('date', 'ad_id') \
        .annotate(count=Count('ad_id')).values('ad_id', 'date', 'count').filter(time__day=datetime.now().day)
    views = View.objects.annotate(date=TruncDay('time')).values('date', 'ad_id') \
        .annotate(count=Count('ad_id')).values('ad_id', 'date', 'count').filter(time__day=datetime.now().day)
    report = ReportDaily.objects
    for ad in Ad.objects.values_list('pk'):
        report.create(ad_id=ad, clicks=clicks.get(ad_id=ad, default=0), time=datetime.now(), views=views.get(ad_id=ad),
                      default=0)
