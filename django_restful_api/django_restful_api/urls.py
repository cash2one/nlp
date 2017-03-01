from django.conf.urls import url
from django.contrib import admin

from nlp_app import views as nlp_views

urlpatterns = [
    url(r'^add/$', nlp_views.add, name='add'),
    url(r'^$', nlp_views.index, name='home'),
    url(r'^admin/', admin.site.urls),
]
