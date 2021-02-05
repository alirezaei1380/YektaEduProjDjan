from .models import Ad, Advertiser, View, Click
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView, TemplateView
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.db.models import Count
from django.db.models.functions import TruncHour
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from .serializers import AdSerializer, AdvertiserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response


class ReportView(TemplateView, GenericAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    template_name = 'advertiser_management/report.html'

    @staticmethod
    def count(model):
        return model.objects.count()

    @staticmethod
    def get_sum_by_id(model):
        return model.objects.annotate(date=TruncHour('time')).values('date', 'ad_id')\
            .annotate(count=Count('ad_id')).values('ad_id', 'date', 'count')

    @staticmethod
    def get_sum(model):
        return model.objects.annotate(date=TruncHour('time')).values('date').\
            annotate(count=Count('date')).values_list('date', 'count')

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['view_sum'] = list(ReportView.get_sum_by_id(View))
        context['click_sum'] = list(ReportView.get_sum_by_id(Click))
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
            time_difference['ad_id:'+repr(click.ad_id)] = click.time - views.filter(ad_id=click.ad_id, ip=click.ip,
                                                                                    time__lt=click.time)\
                .order_by('-time').first().time
        context['click_view_time_difference_average'] = time_difference
        return context


class AdListView(ListView, ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
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


class AdFormView(CreateView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    model = Ad
    template_name = 'advertiser_management/ad_form.html'
    fields = ['title', 'link', 'image', 'advertiser']
    success_url = 'http://127.0.0.1:8000/advertiser_management/'


class AdView(ModelViewSet):

    serializer_class = AdSerializer
    queryset = Ad.objects.all()

    def list(self, request):
        serializer = AdSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        ad = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data)

    def create(self, request):
        queryset = self.get_queryset()
        queryset.create(request.data)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]