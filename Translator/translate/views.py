from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView, CreateView
from django.urls import reverse
from django.contrib import messages

from translate.forms import LogInForm, SignUpForm, TranslatorForm
from translate.models import User, Translation
from translator import settings


class LoginProhibitedMixin:
    """The LoginProhibitedMixin is used to prevent logged in users from accessing the login and signup pages.
    It is adapted from the Clucker project from 5CCS2SEG."""
    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured('LoginProhibitedMixin requires either a value for '  # pragma: no cover
                                       'redirect_when_logged_in_url or an implementation '
                                       'for get_redirect_when_logged_in_url().')
        else:
            return self.redirect_when_logged_in_url


class HomeView(View):
    """View that shows the home page."""
    template_name = 'home.html'
    translated_text = ''
    text = ''
    form = TranslatorForm()

    def get(self, request):
        translation_pk = request.GET.get('translation', None)
        if translation_pk:
            translation = Translation.objects.get(pk=translation_pk)
            self.form = TranslatorForm(initial={'text': translation.text, 'language': translation.input_language})

        return self.render()

    def post(self, request):
        self.form = TranslatorForm(request.POST)
        if self.form.is_valid():
            self.translated_text = self.form.translate()

            # try to find an existing translation
            try:
                translation = Translation.objects.get(
                    text=self.form.cleaned_data['text'],
                    input_language=self.form.cleaned_data['language'],
                    user_id=request.user.pk
                )
                translation.translated_text = self.translated_text
                translation.save()
            except Translation.DoesNotExist:
                # create a new translation
                translation = Translation.objects.create(
                    text=self.form.cleaned_data['text'],
                    translated_text=self.translated_text,
                    user_id=request.user.pk,
                    input_language=self.form.cleaned_data['language']
                )

            translation.save()
            self.text = self.form.cleaned_data['text']

        return self.render()

    def render(self):
        return render(self.request, self.template_name,
                      {'form': self.form, 'text': self.text, 'translations': self.translated_text,
                       'second_language': self.get_second_language()})

    def get_second_language(self):
        try:
            if self.form.cleaned_data['language'] == 'English':
                return 'Polish'
            else:
                return 'English'
        except AttributeError:
            return 'Polish'


class LogInView(LoginProhibitedMixin, View):
    """View that logs in user. The structure was inspired by the Clucker project from 5CCS2SEG."""
    template_name = 'login.html'
    next_page = '/'
    form_class = LogInForm
    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.LOGIN_REDIRECT_URL

    def get(self, request):
        self.next_page = request.GET.get('next') or '/'
        return self.render()

    def post(self, request):
        form = self.form_class(request.POST)
        self.next_page = request.POST.get('next') or settings.LOGIN_REDIRECT_URL
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next_page)
        messages.add_message(request, messages.ERROR, 'The provided credentials were invalid!')
        return self.render()

    def render(self):
        return render(self.request, self.template_name, {'form': self.form_class, 'next': self.next_page})


class LogOutView(LoginRequiredMixin, LogoutView):
    next_page = '/'
    success_url = '/'
    template_name = 'logout.html'
    login_url = '/login/'


class SignUpView(LoginProhibitedMixin, CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    redirect_when_logged_in_url = settings.LOGIN_REDIRECT_URL
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        form.save()
        login(self.request, form.instance)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(self.success_url)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        # can only view your own profile
        if user != self.request.user:
            raise Http404
        translations = Translation.objects.filter(user=user)
        # sort translations by date
        translations = translations.order_by('-updated_at')
        context['translations'] = translations
        return context

    def get(self, request, *args, **kwargs):
        try:
            return super(ProfileView, self).get(request, *args, **kwargs)
        except Http404:
            return redirect('home')


class PasswordChangeView(LoginRequiredMixin, View):
    template_name = 'password_change.html'
    success_url = '/'
    form_class = PasswordChangeForm

    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        messages.add_message(request, messages.ERROR, 'The provided credentials were invalid!')
        return render(request, self.template_name, {'form': form})
