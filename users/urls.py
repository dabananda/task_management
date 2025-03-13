from django.urls import path
from users.views import sign_up, log_in, signout, activate_user, admin_dashboard, assign_rule, create_group, group_list

urlpatterns = [
    path("sign-up", sign_up, name="sign-up"),
    path("log-in", log_in, name="log-in"),
    path("signout", signout, name="signout"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("admin/dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/<int:user_id>/assign-rule/", assign_rule, name="assign-rule"),
    path("admin/create-group/", create_group, name="crete-group"),
    path("admin/group-list/", group_list, name="group-list")
]
