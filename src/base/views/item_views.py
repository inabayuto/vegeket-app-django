# 商品一覧・商品詳細ページのViewを定義したモジュール。
# Itemモデルを用いてトップページと商品詳細ページを表示。

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Item

# トップページ用View。全商品を一覧表示。
class IndexListView(ListView):
    model = Item  # 商品モデルを利用
    template_name = "pages/index.html"  # 使用テンプレート

# 商品詳細ページ用View。商品IDで1件取得し詳細表示。
class ItemDetailView(DetailView):
    model =  Item  # 商品モデルを利用
    template_name = "pages/item.html"  # 使用テンプレート



