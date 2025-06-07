# ユーザー・プロフィール管理用のモデル定義モジュール。
# カスタムユーザーモデル、プロフィール、OneToOne自動生成シグナルを実装。

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from base.models import create_id
 
# ユーザー作成・管理用のカスタムマネージャ。
class UserManager(BaseUserManager):
 
    def create_user(self, username, email, password=None):
        # email必須チェック
        if not email:
            raise ValueError('Users must have an email address')
        # ユーザーインスタンス生成
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)  # パスワードハッシュ化
        user.save(using=self._db)
        return user
 
    def create_superuser(self, username, email, password=None):
        # スーパーユーザー作成
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
 
# カスタムユーザーモデル。IDはランダム文字列、ユーザー名・メール・管理フラグ等を保持。
class User(AbstractBaseUser):
    id = models.CharField(default=create_id, primary_key=True, max_length=22)  # ランダムID
    username = models.CharField(
        max_length=50, unique=True, blank=True, default='匿名')  # ユーザー名
    email = models.EmailField(max_length=255, unique=True)  # メールアドレス
    is_active = models.BooleanField(default=True)  # 有効フラグ
    is_admin = models.BooleanField(default=False)  # 管理者フラグ
    objects = UserManager()  # カスタムマネージャ
    USERNAME_FIELD = 'username'  # 認証用フィールド
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]
 
    def __str__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        "特定パーミッションを持つか（常にTrue返却）"
        return True
 
    def has_module_perms(self, app_label):
        "特定アプリのパーミッションを持つか（常にTrue返却）"
        return True
 
    @property
    def is_staff(self):
        "スタッフ権限かどうか（is_adminと連動）"
        return self.is_admin
 
# ユーザーのプロフィール情報を保持するモデル。OneToOneでUserと紐付く。
class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)  # ユーザーと1対1
    name = models.CharField(default='', blank=True, max_length=50)  # 氏名
    zipcode = models.CharField(default='', blank=True, max_length=8)  # 郵便番号
    prefecture = models.CharField(default='', blank=True, max_length=50)  # 都道府県
    city = models.CharField(default='', blank=True, max_length=50)  # 市区町村
    address1 = models.CharField(default='', blank=True, max_length=50)  # 番地
    address2 = models.CharField(default='', blank=True, max_length=50)  # 建物名等
    tel = models.CharField(default='', blank=True, max_length=15)  # 電話番号
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
 
    def __str__(self):
        return self.name
 
# User作成時にProfileも自動生成するシグナルレシーバ。
@receiver(post_save, sender=User)
def create_onetoone(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])  # 新規ユーザー時にプロフィール作成