from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ad_id>/', views.AdRedirectView.as_view(), name='ad_link'),
    path('ad_form/', views.AdFormView.as_view(), name='AdView')
]