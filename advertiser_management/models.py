from django.db import models


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
    ad_id = models.IntegerField()
    time = models.DateTimeField()
    ip = models.CharField(max_length=50)

    class Meta:
        abstract = True


class View(CommonInfo):
    pass


class Click(CommonInfo):
    pass

