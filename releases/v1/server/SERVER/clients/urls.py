from django.urls import path, include
from . import views
from django.contrib.auth.views import login
from django.conf.urls.static import static
from django.conf import settings
from .forms import Login_Form


urlpatterns = [

    #path('login/', login(authentication_form=Login_Form), {"template_name" : "registration/login.html"}),
    path('', views.HomePage, name= 'homepage'),
    path('login/', views.Login, name = "login"),
    path('signup/', views.SignUP, name = 'signup'),
    path('add_devices/', views.Register_devices, name = "register"),
    path('device_list/', views.Device_info, name = "device_info"),
    path('logout/', views.Logout),
    path('reset_password/', views.Reset )



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


