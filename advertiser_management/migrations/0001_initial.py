# Generated by Django 3.1.5 on 2021-01-24 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('views', models.IntegerField(auto_created=True, default=0)),
                ('clicks', models.IntegerField(auto_created=True, default=0)),
                ('id', models.IntegerField(auto_created=True, default=17527, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
