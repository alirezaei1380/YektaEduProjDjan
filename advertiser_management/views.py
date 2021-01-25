from django.shortcuts import render, redirect
from .models import Ad
from .models import Advertiser
from django.views.generic.edit import CreateView


def index(request):
    context = {'advertisers': Advertiser.objects.iterator()}
    for ad in Ad.objects.all():
        ad.save()
        ad.advertiser.save()
    return render(request, 'advertiser_management/ads.html', context=context)


def ad(request, ad_id):
    ad = Ad.get_ad(ad_id)
    ad.save()
    return redirect(ad.link)


class AdView(CreateView):
    model = Ad
    template_name = 'advertiser_management/ad_form.html'
    fields = ['title', 'link', 'image', 'advertiser']
    success_url = 'http://127.0.0.1:8000/advertiser_management/'
