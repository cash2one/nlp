from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from nlp_app import views as nlp_views

urlpatterns = [
                  url(r'^v1/demo/word_seg/$', nlp_views.word_seg, name='word_seg'),
                  url(r'^v1/demo/key/$', nlp_views.key, name='key'),
                  # url(r'^$', nlp_views.index, name='home'),
                  # url(r'^admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
