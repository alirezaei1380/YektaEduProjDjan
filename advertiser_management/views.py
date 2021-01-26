from django.shortcuts import render
from .models import Ad
from .models import Advertiser
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404


def index(request):
    context = {'advertisers': Advertiser.objects.iterator()}
    return render(request, 'advertiser_management/ads.html', context=context)


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
