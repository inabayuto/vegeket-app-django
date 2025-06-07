# 決済・支払い処理に関するViewを集約したモジュール。
# Stripeを用いた決済フロー、決済成功・キャンセル画面、税率設定、カート情報の整形処理などを提供。

from django.shortcuts import redirect
from django.views.generic import ListView, View, TemplateView
from base.models import Item
from django.conf import settings
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin

# StripeのAPIキーを設定
stripe.api_key = settings.STRIPE_API_SECRET_KEY

# 決済成功時の画面を表示するView。カート情報をセッションから削除。
class PaySuccessView(LoginRequiredMixin, TemplateView):
    template_name =  'pages/success.html'

    def get(self, request, *args, **kwargs):
        # 決済完了後、カート情報をセッションから削除
        del request.session['cart']
        return super().get(request, *args, **kwargs)

# 決済キャンセル時の画面を表示するView。
class PayCancelView(LoginRequiredMixin, TemplateView):
     template_name = 'pages/cancel.html'

     def get(self, request, *args, **kwargs):
         return super().get(request, *args, **kwargs)

# Stripeの消費税率オブジェクトを作成。日本の消費税を想定。
tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)

# Stripeのline_items用に商品情報を整形する関数。
def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'JPY',
            'unit_amount': unit_amount,  # 商品単価（税抜）
            'product_data': {'name': name, }
        },
        'quantity': quantity,  # 購入数
        'tax_rates': [tax_rate.id]  # 適用する税率ID
    }

# プロフィール情報が全て入力済みかチェックする関数。
def check_profile_filled(profile):
    if profile.name is None or profile.name == '':
        return False
    elif profile.zipcode is None or profile.zipcode == '':
        return False
    elif profile.prefecture is None or profile.prefecture == '':
        return False
    elif profile.city is None or profile.city == '':
        return False
    elif profile.address1 is None or profile.address1 == '':
        return False
    return True

# Stripe決済用のView。カート情報からline_itemsを生成し、StripeのCheckout Sessionを作成。
class PayWithStripe(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        # プロフィールが全て入力済みかチェック。不足があればプロフィール編集画面へリダイレクト。
        if not check_profile_filled(request.user.profile):
            return redirect('/profile/')
        # セッションからカート情報を取得。空ならトップページへリダイレクト。
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            return redirect('/')
        # Stripe用line_itemsリストを生成
        line_items = []
        for item_pk, quantity in cart['items'].items():
            # 商品IDから商品情報を取得
            item = Item.objects.get(pk=item_pk)
            # line_itemを作成しリストに追加
            line_item = create_line_item(
                item.price, item.name, quantity)
            line_items.append(line_item)
        # StripeのCheckout Sessionを作成
        checkout_session = stripe.checkout.Session.create(
            # customer_email=request.user.email,  # 必要に応じて有効化
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://0.0.0.0:8000/pay/success/',
            cancel_url='http://0.0.0.0:8000/pay/cancel/',
        )
        # Stripeの決済ページへリダイレクト
        return redirect(checkout_session.url)