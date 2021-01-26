from django.urls import path


from . import views

urlpatterns = [
    path('', views.AdListView.as_view(), name='AdListView'),
    path('<int:ad_id>/', views.AdRedirectView.as_view(), name='ad_link'),
    path('ad_form/', views.AdFormView.as_view(), name='AdFormView')
]
