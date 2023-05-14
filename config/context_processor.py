from user.forma import AuthenticationAjaxForm


def get_context_data(requests):
    context = {
        'login_ajax': AuthenticationAjaxForm,
    }
    return context