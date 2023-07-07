from django.urls import include, path

urlpatterns = [
    path('', include('pdf_app.urls')),
]
