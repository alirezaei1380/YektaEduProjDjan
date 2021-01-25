from django.db import models


class Advertiser(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.AutoField(primary_key=True)
    clicks = models.IntegerField(default=0, auto_created=True, editable=False)
    views = models.IntegerField(default=0, auto_created=True, editable=False)


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    clicks = models.IntegerField(default=0, auto_created=True, editable=False)
    views = models.IntegerField(default=0, auto_created=True, editable=False)
    link = models.CharField(max_length=100)
    image = models.ImageField(default='', upload_to='images/')
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    @staticmethod
    def get_ad(ad_id):
        for ad in Ad.objects.all():
            if ad.id == ad_id:
                return ad
