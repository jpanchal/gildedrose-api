from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView, UserView, UserDetailsView, RegisterUsers
from .views import CartCreateView, CartDetailsView
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = {
    url(r'^itemlists/$', CreateView.as_view(), name="create"),
    url(r'^itemlists/(?P<pk>[0-9]+)/$',
        DetailsView.as_view(), name="details"),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$',
        UserDetailsView.as_view(), name="user_details"),
    url(r'^get-token/', obtain_auth_token),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    url(r'^buyitem/$', CartCreateView.as_view(), name="create"),
    url(r'^buyitem/(?P<pk>[0-9]+)/$',
        CartDetailsView.as_view(), name="details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
