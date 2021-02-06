from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('', views.AdListView.as_view(), name='AdListView'),
    path('<int:ad_id>/', views.AdRedirectView.as_view(), name='ad_link'),
    path('ad_form/', views.AdFormView.as_view(), name='AdFormView'),
    path('report/', views.ReportView.as_view(), name='ReportView'),
    path('api/advertiser_management/report', views.AdView.as_view({
        'get': 'report'
    }))
]

router = DefaultRouter()
router.register(r'api/advertiser_management/ad', views.AdView, basename='Ad')
router.register(r'api/advertiser_management/advertiser', views.AdvertiserView, basename='Advertiser')
router.register(r'api/advertiser_management/click', views.ClickView, basename='Click')
router.register(r'api/advertiser_management/view', views.ViewView, basename='View')
urlpatterns += router.urls
