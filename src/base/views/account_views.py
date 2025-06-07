# アカウント関連のビューをまとめたファイル。
# ユーザー登録、ログイン、アカウント情報・プロフィール編集のViewを定義。

from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from base.models import Profile
from base.forms import UserCreationForm
from django.contrib import messages

# ユーザー新規登録用のView。CreateViewを継承し、Userモデルとカスタムフォームを利用。
class SignUpView(CreateView):
    model = get_user_model()
    form_class =  UserCreationForm
    success_url = '/login/'
    template_name = 'pages/login_signup.html'

    def form_valid(self, form):
        messages.success(self.request, 'ユーザー登録が完了しました。')
        return super().form_valid(form)

# ログイン用のView。Django標準のLoginViewを継承。
class Login(LoginView):
    template_name = 'pages/login_signup.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログインしました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ログインに失敗しました。')
        return super().form_invalid(form)

# アカウント情報（ユーザー名・メールアドレス）編集用のView。
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ('username', 'email')
    success_url = '/account/'

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

    def form_valid(self, form):
        messages.success(self.request, 'アカウント情報を更新しました。')
        return super().form_valid(form)

# プロフィール情報編集用のView。
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    fields = ('name', 'zipcode', 'prefecture',
              'city', 'address1', 'address2', 'tel')
    success_url = '/profile/'
 
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

    def form_valid(self, form):
        messages.success(self.request, 'プロフィール情報を更新しました。')
        return super().form_valid(form)