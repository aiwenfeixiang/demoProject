"""otherDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.static import serve

from ckeditor_uploader import views as ck_views

from web import views


sentry_urlpatterns = [
    url(r'^$', views.sentry_demo),
]

ckeditor_urlpatterns = [
    # 图片上传处理
    url(r'upload/', ck_views.upload),
    url(r'browse/', ck_views.browse, name='ckeditor_browse'),
]

logging_urlpatterns = [
    # error demo
    url(r'', views.log),
]

video_urlpatterns = [
    url(r'play/', views.play),
    url(r'verify/', views.verify)
]

email_urlpatterns = [
    url("send_mail/", views.send_mail)
]

jwt_urlpatterns = [
    url("", views.jwt)
]

rw_urlpatterns = [
    url(r"", views.rw)
]

celery_urlpatterns = [
    url(r"", views.delay_task)
]

wx_urlpatterns = [
    url(r"msg", views.send_template)
]

ali_urlpatterns = [
    url(r"pay", views.ali_pay),
    url(r"sms", views.ali_sms)
]

urlpatterns = [
    # `admin` 路由
    url(r'^admin/', admin.site.urls),
    # `sentry` 示例
    url(r'^sentry/', include(sentry_urlpatterns)),
    # `ck-editor` 示例
    url(r'^ckeditor/', include(ckeditor_urlpatterns)),
    # `logging` 示例
    url(r'^log/', include(logging_urlpatterns)),
    # `video` 示例(路飞视频业务)
    url(r'^video/', include(video_urlpatterns)),
    # `email` 示例
    url(r'^email/', include(email_urlpatterns)),
    # `jwt` 示例
    url(r'^jwt/', include(jwt_urlpatterns)),
    # `读写分离` 示例
    url(r'^rw/', include(rw_urlpatterns)),
    # 微信相关
    url(r'^wx', include(wx_urlpatterns)),
    # 阿里
    url(r'^ali', include(ali_urlpatterns)),
    # celery
    url(r'celery', include(celery_urlpatterns)),

]

if settings.DEBUG:
    # `media` 文件访问视图
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
