from django.conf.urls import url

from chinese_tutor.views import index
from chinese_tutor.views import export
from chinese_tutor.views import attempt

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^export$', export, name='export'),
    url(r'^attempt/(?P<flash_card_id>[0-9]+)/(?P<value>-?[a-zA-Z-\' ]*)$',
        attempt, name='attempt'),
]
