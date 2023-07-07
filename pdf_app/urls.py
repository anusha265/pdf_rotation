from django.urls import path
from pdf_app import views

app_name = 'pdf_app'

urlpatterns = [
    path('', views.rotate_pdf, name='rotate_pdf'),
]
