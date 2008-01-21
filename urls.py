from django.conf.urls.defaults import *
from django.template import loader, RequestContext

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
)