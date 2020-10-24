from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

# from views import login_view, home, signup_view, logout_view
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # path('accounts/login/', login_view, name='login'),
    # path('accounts/signup/', signup_view, name='signup'),
    # path('accounts/logout/', logout_view, name='logout'),