from django.urls import path, include
from django.views.generic import TemplateView

from user.views import Register, EmailVerify, Login, LoginAjaxView

urlpatterns = [
    path('login/', Login.as_view(), name='login'),

    path('', include('django.contrib.auth.urls')),

    path('invalid_verify/', TemplateView.as_view(template_name='registration/invalid_verify.html'), name='invalid_verify'),

    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),

    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),

    path('register/', Register.as_view(), name='register'),

    path('login_ajax/', LoginAjaxView.as_view(), name='login_ajax'),

]
