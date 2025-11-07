from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('issue/', views.issue_certificate, name='issue_certificate'),
    path('verify/', views.verify_certificate_form, name='verify_form'),
    path('verify/<str:certificate_id>/', views.verify_certificate, name='verify_certificate'),
    path('certificate/<int:pk>/', views.certificate_display, name='certificate_display'),
    path('certificate/<int:pk>/revoke/', views.revoke_certificate, name='revoke_certificate'),
    path('certificate/<int:pk>/reissue/', views.reissue_certificate, name='reissue_certificate'),
    path('certificate/<int:pk>/pdf/', views.certificate_pdf, name='certificate_pdf'),
    path('reset/', views.reset_all, name='reset_all'),
]


