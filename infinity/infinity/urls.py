from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('account/login/', views.login_view, name='login'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/signup/', views.signup_view, name='signup'),
    path('account/profile/', views.profile_view, name='profile'),
    path('account/profile/edit/', views.edit_profile, name='edit_profile'),
    path('account/change-password/', views.change_password, name='change_password'),
    path('reset-password/', PasswordResetView.as_view(template_name="accounts/reset_password.html"), name='reset_password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name="accounts/reset_password_done.html"), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="accounts/reset_password_confirm.html"), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name="accounts/reset_password_complete.html"), name='password_reset_complete'),


    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # path('accounts/login/', login_view, name='login'),
    # path('accounts/signup/', signup_view, name='signup'),
    # path('accounts/logout/', logout_view, name='logout'),
