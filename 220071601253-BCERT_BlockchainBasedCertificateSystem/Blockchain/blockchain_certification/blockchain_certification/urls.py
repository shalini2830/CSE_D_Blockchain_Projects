from django.contrib import admin
from django.urls import path, include
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home_view, name='home'),
    # Auth routes at root for friendly URLs
    path('login/', user_views.login_view, name='login'),
    path('register/', user_views.register_view, name='register'),
    path('logout/', user_views.logout_view, name='logout'),

    # Legacy include still works for /login/ prefixed paths
    path('login/', include('users.urls')),
    path('', include('certificates.urls')),
    path('chain/', include('blockchain.urls')),
]


