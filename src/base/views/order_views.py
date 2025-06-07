# 注文履歴・注文詳細ページのViewを定義したモジュール
# ログインユーザーの注文一覧・詳細表示を提供

from django.views.generic import ListView, DetailView
from base.models import Order
import json
from django.contrib.auth.mixins import LoginRequiredMixin

# 注文履歴一覧ページ用View。ログインユーザーの注文のみを表示
class OrderIndexView(LoginRequiredMixin, ListView):
    model = Order  # 注文モデルを利用
    template_name = "pages/orders.html"  # 使用テンプレート
    ordering = ['-created_at']  # 新しい順に並べる

    def get_queryset(self):
        # ログインユーザーの注文のみ抽出
        return Order.objects.filter(user=self.request.user)

# 注文詳細ページ用View。ログインユーザーの注文のみアクセス可能
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order  # 注文モデルを利用
    template_name = "pages/order.html"  # 使用テンプレート

    def get_queryset(self):
        # ログインユーザーの注文のみ抽出
        return Order.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()  # 注文オブジェクト
        # items, shippingはJSON文字列なので辞書に変換
        context['items'] = json.loads(context['object'].items)
        context['shipping'] = json.loads(context['object'].shipping)
        return context
