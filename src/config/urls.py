from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

     path('', views.IndexListView.as_view()), # トップページ

    #  Item
     path('items/<str:pk>/', views.ItemDetailView.as_view()), # 詳細ページ

    #  Cart
    path('cart/', views.CartListView.as_view()), # カートページ
    path('cart/add/', views.AddCartView.as_view()), # 詳細ページ
    path('cart/remove/<str:item_pk>/', views.remove_from_cart), # 削除ページ

    # Pay
    path('pay/checkout/', views.PayWithStripe.as_view()), # 決済ページ
    path('pay/success/', views.PaySuccessView.as_view()), # 成功ページ
    path('pay/cancel/', views.PayCancelView.as_view()), # キャンセルページ

    # Account
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('account/', views.AccountUpdateView.as_view()),
    path('profile/', views.ProfileUpdateView.as_view()),
]
