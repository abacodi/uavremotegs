from django.conf.urls import url
from . import views

app_name='Generic'
urlpatterns=[
    # Using generic views
    # Index page
    url(r'^$', views.access, name='access'),
    # Users view
    url(r'^home/$', views.HomeView.get_news, name='home'),
    # User info
    url(r'^users/profile$', views.UserView.as_view(), name='userInfo'),
    # Permission denied
    url(r'^permission_denied/$', views.HomeView.permission_denied, name='permission_denied'),
    # logout
    url(r'^logout/$', views.logout_view, name='logout'),
    # Create account
    url(r'^signup/$', views.signup_view, name='signup'),
    # Reset pasword
    url(r'^user/reset_password/$', views.ResetPasswordRequest.as_view(), name='reset'),
    url(r'^user/confirm_reset_pwd/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    # Activation
    url(r'^account_activation_sent/$', views.ActivationView.as_view(), name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]