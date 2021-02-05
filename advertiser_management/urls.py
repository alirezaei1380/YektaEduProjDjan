from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('', views.AdListView.as_view(), name='AdListView'),
    path('<int:ad_id>/', views.AdRedirectView.as_view(), name='ad_link'),
    path('ad_form/', views.AdFormView.as_view(), name='AdFormView'),
    path('report/', views.ReportView.as_view(), name='ReportView')
]

router = DefaultRouter()
router.register(r'api/advertiser_management', views.AdView, basename='Advertiser_management')
urlpatterns += router.urls
