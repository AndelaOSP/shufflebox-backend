from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserView, ProfileView, ShuffleView, HangoutView, \
    BrownbagView, SecretSantaView, HangoutDetailsView, BrownbagDetailsView, \
    BrownbagNextInLineView


urlpatterns = {
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$',
        ProfileView.as_view(), name="profile"),
    url(r'^shuffle/', ShuffleView.as_view()),
    url(r'^hangout/$', HangoutView.as_view(), name="hangout"),
    url(r'^hangout/(?P<pk>[0-9]+)/$',
        HangoutDetailsView.as_view(), name="hangout_details"),
    url(r'^brownbag/$', BrownbagView.as_view(), name="brownbag"),
    url(r'^brownbag/(?P<pk>[0-9]+)/$',
        BrownbagDetailsView.as_view(), name="brownbag_details"),
    url(r'^brownbag/(?P<status>.+)/$', BrownbagNextInLineView.as_view()),
    url(r'^santa/$', SecretSantaView.as_view(), name="santa")
}

urlpatterns = format_suffix_patterns(urlpatterns)
