# 商品一覧・商品詳細ページのViewを定義したモジュール。
# Itemモデルを用いてトップページと商品詳細ページを表示。

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Item, Category, Tag

# トップページ用View。全商品を一覧表示。
class IndexListView(ListView):
    model = Item  # 商品モデルを利用
    template_name = "pages/index.html"  # 使用テンプレート
    queryset = Item.objects.filter(is_published=True)  # 公開フラグがTrueの商品のみ表示するように変更（非公開商品は除外）

# 商品詳細ページ用View。商品IDで1件取得し詳細表示。
class ItemDetailView(DetailView):
    model =  Item  # 商品モデルを利用
    template_name = "pages/item.html"  # 使用テンプレート

# カテゴリごとの商品一覧ページ用View。
class CategoryListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 2
 
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        # 公開フラグがTrueかつ該当カテゴリの商品だけを抽出
        return Item.objects.filter(is_published=True, category=self.category)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Category #{self.category.name}'
        return context
 
# タグごとの商品一覧ページ用View。
class TagListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 2
 
    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        # 公開フラグがTrueかつ該当タグの商品だけを抽出
        return Item.objects.filter(is_published=True, tags=self.tag)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Tag #{self.tag.name}"
        return context



