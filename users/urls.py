from django.urls import path
from users.views import sign_up, log_in, signout, activate_user

urlpatterns = [
    path("sign-up", sign_up, name="sign-up"),
    path("log-in", log_in, name="log-in"),
    path("signout", signout, name="signout"),
    path("activate/<int:user_id>/<str:token>/", activate_user)
]
