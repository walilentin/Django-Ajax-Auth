from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.backends import UserModel
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View

from user.forma import UserCreationForm, AuthenticationForm
from user.utils import send_email_verify

from django.contrib.auth.tokens import default_token_generator as token_generator

from django.http import JsonResponse

User = get_user_model()


class LoginAjaxView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={}, status=201)
            return JsonResponse(
                data={'error': 'Login and password invalid'},
                status=400
            )
        return JsonResponse(
            data={'error': 'Enter login and password'},
            status=400
        )


class Login(LoginView):
    form_class = AuthenticationForm


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user


class Register(View):
    template_name = 'Registration/register.html'

    def get(self, requests):
        context = {
            'form': UserCreationForm()
        }
        return render(requests, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            # name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_verify(request, user)
            return redirect('confirm_email')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
