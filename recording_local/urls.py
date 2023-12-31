"""
URL configuration for recording_local project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from webapi.views import record_control as views
from typing import List


urlpatterns: List = [
    path('env', views.CheckEnvView.as_view()),
    path('record/disk_check', views.CheckDiskView.as_view()),
    path('record/set_scene', views.SelectSceneView.as_view()),
    path('record/start', views.StartRecordView.as_view()),
    path('record/stop', views.StopRecordView.as_view()),
]
