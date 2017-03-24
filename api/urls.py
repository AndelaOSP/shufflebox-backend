from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserView, ProfileView, ShuffleView, HangoutView, \
    BrownbagView, SecretSantaView, HangoutDetailsView, BrownbagDetailsView, \
    BrownbagNextInLineView, BrownbagUserListView, SecretSantaDetailsView


urlpatterns = {
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$',
        ProfileView.as_view(), name="profile"),
    url(r'^shuffle/', ShuffleView.as_view()),
    url(r'^hangouts/$', HangoutView.as_view(), name="hangout"),
    url(r'^hangouts/(?P<pk>[0-9]+)/$',
        HangoutDetailsView.as_view(), name="hangout_details"),
    url(r'^brownbags/$', BrownbagView.as_view(), name="brownbag"),
    url(r'^brownbags/(?P<pk>[0-9]+)/$',
        BrownbagDetailsView.as_view(), name="brownbag_details"),
    url(r'^brownbags/next/$', BrownbagNextInLineView.as_view()),
    url(r'brownbags/not_presented/', BrownbagUserListView.as_view()),
    url(r'^santas/$', SecretSantaView.as_view(), name="santa"),
    url(r'^santas/(?P<pk>[0-9]+)/$',
        SecretSantaDetailsView.as_view(), name="santa_details")
}

urlpatterns = format_suffix_patterns(urlpatterns)