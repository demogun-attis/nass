"""nass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^input$', views.sprinkle_all,name="sprinkle_now"),
    url(r'^individual$', views.individual,name="individual_runner"),
    url(r'^valve_switch.*$', views.valve_switch,name="valve_switch"),
    url(r'^stop_process.*$', views.stop_process,name="stop_process"),
    url(r'^program_page.*$', views.program_page,name="program_page"),
    url(r'^$', views.button),
    url(r'^$', views.sprinkle_all),
    url(r'^output', views.output,name="script"),
]
