from . import views
from django.urls import path, include

urlpatterns = [
    path('save/', views.saveAccount, name='save'),
    path('login/', views.loginView, name='login'),
    path('authenticate', views.authenticate_defined, name='authenticate_defined'),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(), name='activate'),
]