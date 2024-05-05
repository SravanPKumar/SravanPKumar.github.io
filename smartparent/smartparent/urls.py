"""smartparent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from smartapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('ureg/',views.ureg),
    path('login/',views.login),
    path('useraction/',views.useraction),
    path('loginaction/',views.loginaction),
    path('userview/',views.userview),
    path('userhome/',views.userhome),
    path('adminhome/',views.adminhome),
    path('doctorhome/',views.doctorhome),
    path('dreg/',views.dreg),
    path('dregaction/',views.dregaction),
    path('viewdoctor/',views.viewdoctor),
    path('accept/',views.accept),
    path('reject/',views.reject),
    path('index/',views.index),
    path('dprofile/',views.dprofile),
    path('updatedprofile/',views.updatedprofile),
    path('question/',views.questions),
    path('addquestions/',views.addquestions),
    # path('addquestionaction/',views.addquestionaction),
    path('delquestions/',views.delquestions),
    path('personascan/',views.personascan),
    path('peraction/',views.peraction),
    path('prediction/',views.prediction),
    path('doctorconsult/',views.doctorconsult),
    path('counsellorconsult/',views.counsellorconsult),
    path('uViewDoctor/',views.uViewDoctor),
    path('book/',views.book),
    path('Ubookstatus/',views.Ubookstatus),
    path('doctorviewbook/',views.doctorviewbook),
    path('baccept/',views.baccept),
    path('breject/',views.breject),
    path('feedback/',views.feedback),
    path('feedaction/',views.feedaction),
    path('taction/',views.taction),
    path('uViewCounsellor/',views.uViewCounsellor),
    path('bookc/',views.bookc),
    path('bookcaction/',views.bookcaction),
    path('bookD/',views.bookD),
    path('counsellorhome/',views.counsellorhome),
    path('viewfeedback/',views.viewfeedback),
    path('reports/',views.reports),
    path('utime/',views.utime),



    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()

    
