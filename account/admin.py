from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin
from .models import UploadedFile, Student, DynamicColumn
from .models import SchoolClass

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'teacher', 'get_students', 'get_teaching_assistants')
    search_fields = ('class_name', 'teacher__username')
    list_filter = ('teacher',)

    def get_students(self, obj):
        return ", ".join([student.full_name for student in obj.students.all()])
    get_students.short_description = "دانش‌آموزان"

    def get_teaching_assistants(self, obj):
        return ", ".join([ta.username for ta in obj.teaching_assistants.all()])
    get_teaching_assistants.short_description = "دستیاران آموزشی"
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address', 'major', 'birth_date', 'postal_code', 'father_job', 'tuition_fee', 'user_type')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(DynamicColumn)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at', 'extracted_text_preview')
    search_fields = ('file', 'uploaded_at')

    def extracted_text_preview(self, obj):
        return obj.extracted_text[:100] + "..." if obj.extracted_text else "بدون متن"
    extracted_text_preview.short_description = "پیش‌نمایش متن استخراج شده"
