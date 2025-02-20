from django.urls import path
from . import views
from .views import (
    register_view, logout_view, CustomLoginView,
    profile_view, edit_profile_view,
    forgot_password_view, verify_otp_view, reset_password_view, admin_dashboard,
    add_student_view, edit_student_view, delete_student_view, add_dynamic_column, add_school_class,
    edit_school_class, delete_school_class, chat_with_ai, reset_chat  # اضافه کردن این خط
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile_view, name="edit_profile"),
    path("forgot-password/", forgot_password_view, name="forgot_password"),
    path("verify-otp/", verify_otp_view, name="verify_otp"),
    path("reset-password/<str:email>/", reset_password_view, name="reset_password"),
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
    path('add-student/', add_student_view, name='add_student'),  # اضافه کردن این خط
    path('edit-student/<int:student_id>/', edit_student_view, name='edit_student'),
    path('delete-student/<int:student_id>/', delete_student_view, name='delete_student'),
    path('add-column/', add_dynamic_column, name='add_column'),
    path('add-school-class/', add_school_class, name='add_school_class'),
    path('edit-school-class/<int:class_id>/', edit_school_class, name='edit_school_class'),
    path('delete-school-class/<int:class_id>/', delete_school_class, name='delete_school_class'),
    path('chat/', chat_with_ai, name='chat_with_ai'),
    path('chat/reset/', reset_chat, name='reset_chat'),
]
