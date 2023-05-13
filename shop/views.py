from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from user.forma import UserCreationForm


class Index(View):
    template_name = 'index.html'

    def get(self, requests):
        context = {
            'form': UserCreationForm()
        }
        return render(requests, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
