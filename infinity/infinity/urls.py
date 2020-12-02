from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home, name='home'),
    path('', include('blog.urls')),
    path('', include('users.urls')),

    

    path('summernote/', include('django_summernote.urls')),
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
