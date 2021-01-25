from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ad_id>/', views.ad, name='ad'),
    path('ad_form/', views.AdView.as_view(), name='AdView')
]