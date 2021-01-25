from .models import View
from .models import Ad
from .models import Click
import datetime
import re


class ViewMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.endswith("advertiser_management/"):
            for ad in Ad.objects.all():
                view = View(ad_id=ad.id, time=datetime.datetime.now(), ip=request.META.get('HTTP_X_FORWARDED_FOR'))
                view.save()
        response = self.get_response(request)
        return response


class ClickMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        match = re.match("/advertiser_management/(\d+)/", request.path)
        if match:
            click = Click(ad_id=match.group(1), time=datetime.datetime.now(), ip=request.META.get('HTTP_X_FORWARDED_FOR'))
            click.save()
        response = self.get_response(request)
        return response
