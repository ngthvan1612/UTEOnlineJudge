from django.contrib.auth.decorators import user_passes_test
from backend.views.settings import REDIRECT_FIELD_NAME

def admin_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='/login/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
