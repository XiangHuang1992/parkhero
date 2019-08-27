from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from apps.users.forms import UserChangeForm, UserCreationForm
from .models import BlackList, VerificationCode

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "verification_code", "created_time"]
    list_filter = ["phone_number"]
    search_fields = ["phone_number"]
    ordering = ["created_time"]


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "plate_number",
        "user_id",
        "amount",
        "blacking",
        "created_time",
        "update_time",
        "memo",
    ]
    list_filter = [
        "uuid",
        "plate_number",
        "user_id",
        "amount",
        "blacking",
        "created_time",
        "update_time",
        "memo",
    ]
    ordering = ["user_id"]
