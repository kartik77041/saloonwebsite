from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name = 'home'),
    path('handlelogin', views.handleLogin, name = 'handleLogin'),
    path('handlelogout', views.handlelogout, name = 'handeLogout'),
    path('services', views.services, name = 'services'),
    path('scheduling/', views.schedule, name = 'scheduling'),
    path('updates/', views.updates, name = 'updates'),
    path('postcomment/', views.postComment, name = 'postcomment'),
    path('academy', views.academy, name = 'academy'),
    path('verify/<auth_token>', views.verify, name='verify'),  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)