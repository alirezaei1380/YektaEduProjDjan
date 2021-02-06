from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Advertiser(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    image = models.ImageField(default='', upload_to='images/')
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CommonInfo(models.Model):
    #ad_id = models.ForeignKey(Ad, models.CASCADE)
    ad_id = models.IntegerField()
    time = models.DateTimeField()
    ip = models.CharField(max_length=50)

    class Meta:
        abstract = True


class View(CommonInfo):
    pass


class Click(CommonInfo):
    pass


class CommonReportInfo(models.Model):

    #ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    ad_id = models.IntegerField()
    time = models.DateTimeField()
    views = models.IntegerField()
    clicks = models.IntegerField()


class ReportHourly(CommonReportInfo):
    pass


class ReportDaily(CommonReportInfo):
    pass
