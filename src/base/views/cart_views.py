# カート機能に関するViewを集約したモジュール。
# カート一覧表示、商品追加、商品削除のロジックを提供。

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.views.generic import ListView, View
from base.models import Item
from django.conf import settings
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# カート一覧ページ用View。セッションからカート情報を取得し、合計金額や税込金額も計算。
class CartListView(LoginRequiredMixin, ListView):
    model =  Item  # 商品モデルを利用
    template_name = 'pages/cart.html'  # 使用するテンプレート
 
    def get_queryset(self):
        # セッションからカート情報を取得
        cart = self.request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            # カートが空の場合はトップページにリダイレクト
            return redirect('/')
        self.queryset = []  # 商品オブジェクト格納用リスト
        self.total = 0  # 小計初期化
        for item_pk, quantity in cart['items'].items():
            # 商品IDから商品情報を取得
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity  # カート内数量をセット
            obj.subtotal = int(obj.price * quantity)  # 小計計算
            self.queryset.append(obj)  # 商品リストに追加
            self.total += obj.subtotal  # 小計を加算
        # 税込合計を計算
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        # セッションのカート情報を更新
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        print(cart)  # デバッグ用出力
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        # テンプレートに渡すコンテキストを拡張
        context = super().get_context_data(**kwargs)
        try:
            context["total"] = self.total  # 小計
            context["tax_included_total"] = self.tax_included_total  # 税込合計
        except Exception:
            pass  # 初回アクセス時などはスルー
        return context

# カートに商品を追加するためのView。POSTリクエストで商品IDと数量を受け取り、セッションに保存。
class AddCartView(LoginRequiredMixin, View):
    def post(self, request):
        # POSTデータから商品IDと数量を取得
        item_pk =  request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        # セッションからカート情報を取得
        cart =  request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            # カートが空の場合は新規作成
            items = OrderedDict()
            cart = {'items': items}
        # 既にカートに商品がある場合は数量を加算、なければ新規追加
        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        else:
            cart['items'][item_pk] = quantity
        # セッションにカート情報を保存
        request.session['cart'] = cart
        return redirect('/cart/')

# カートから商品を削除する関数ベースView。ログイン必須。
@login_required  
def remove_from_cart(request, item_pk):
    # セッションからカート情報を取得
    cart = request.session.get('cart', None)
    if cart is not None:
        # 指定商品をカートから削除
        del cart['items'][item_pk]
        # セッションにカート情報を保存
        request.session['cart'] = cart
    return redirect('/cart/')