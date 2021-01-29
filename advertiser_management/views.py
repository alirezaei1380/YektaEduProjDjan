from .models import Ad, Advertiser, View, Click
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView, TemplateView
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.db.models import Count, F
from django.db.models.functions import TruncHour
import datetime


class ReportView(TemplateView):
    template_name = 'advertiser_management/report.html'

    @staticmethod
    def count(model):
        return model.objects.count()

    @staticmethod
    def get_sum_by_id(model):
        return model.objects.annotate(date=TruncHour('time')).values('date', 'ad_id')\
            .annotate(count=Count('ad_id')).values('date', 'ad_id', 'count')

    @staticmethod
    def get_sum(model):
        return model.objects.annotate(date=TruncHour('time')).values('date').\
            annotate(count=Count('date')).values_list('date', 'count')

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['view_sum'] = ReportView.get_sum_by_id(View)
        context['click_sum'] = ReportView.get_sum_by_id(Click)
        context['click_view_rate_sum'] = ReportView.count(Click) / ReportView.count(View)
        views = list(ReportView.get_sum(View))
        clicks = dict(ReportView.get_sum(Click))
        click_view_rate = {}
        for view in views:
            click_view_rate[view[0]] = clicks.get(view[0], 0) / view[1]
        context['click_view_rate'] = {k: v for k, v in sorted(click_view_rate.items(),
                                                              key=lambda item: item[1], reverse=True)}
        time_difference = {}
        clicks = Click.objects.all()
        views = View.objects.all()
        for click in clicks:
            time_difference['ad_id:'+click.ad_id.__str__()] = click.time - views.filter(ad_id=click.ad_id, ip=click.ip)\
                .order_by('time').first().time
        context['click_view_time_difference_average'] = time_difference
        return context


class AdListView(ListView):
    model = Advertiser
    template_name = 'advertiser_management/ad_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdListView, self).get_context_data(**kwargs)
        return context


class AdRedirectView(RedirectView):
    pattern_name = 'ad_link'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, id=kwargs['ad_id'])
        return ad.link


class AdFormView(CreateView):
    model = Ad
    template_name = 'advertiser_management/ad_form.html'
    fields = ['title', 'link', 'image', 'advertiser']
    success_url = 'http://127.0.0.1:8000/advertiser_management/'
