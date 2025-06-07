# 注文(Order)管理用のモデル定義モジュール。
# create_idによるユニークなID生成を利用し、注文情報・配送情報・状態管理を行う。

from django.db import models
from django.contrib.auth import get_user_model
from base.models import create_id

class Order(models.Model):
    # 年月日時分秒」形式のIDを生成していると、同じ秒内に複数注文が発生するとIDが重複するため、create_idでランダムなユニークIDを生成する
    id = models.CharField(primary_key=True, default=create_id, max_length=22, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # 注文者（ユーザー）
    uid = models.CharField(editable=False, max_length=50)  # ユーザーIDの複製（検索・参照用）
    is_confirmed = models.BooleanField(default=False)  # 注文確定フラグ
    amount = models.PositiveIntegerField(default=0)  # 税抜合計金額
    tax_included = models.PositiveIntegerField(default=0)  # 税込合計金額
    items = models.JSONField()  # 注文商品情報（JSON形式で保存）
    shipping = models.JSONField()  # 配送先情報（JSON形式で保存）
    shipped_at = models.DateTimeField(blank=True, null=True)  # 発送日時
    canceled_at = models.DateTimeField(blank=True, null=True)  # キャンセル日時
    memo = models.TextField(blank=True)  # 管理者用メモ
    created_at = models.DateTimeField(auto_now_add=True)  # 注文作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 注文更新日時
 
    def __str__(self):
        # 管理画面等での表示用（IDを返す）
        return self.id