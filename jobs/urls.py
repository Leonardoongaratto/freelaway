from django.urls import path
from . import views


urlpatterns = [
    path('find_jobs/', views.find_jobs, name="find_jobs"),
    path('aceitar_job/<int:id>/', views.aceitar_job, name="aceitar_job"),
    path('perfil/', views.perfil, name="perfil")
]