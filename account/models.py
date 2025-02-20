# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import os
import markdown

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('visitor', 'بازدیدکننده'),
        ('admin', 'ادمین'),
        ('flight_student', 'دانشجوی پرواز'),
        ('beginner_student', 'دانشجو آغاز'),
    ]

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    father_job = models.CharField(max_length=100, blank=True, null=True)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='visitor')
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    national_code = models.CharField(
        max_length=10, unique=True, verbose_name="کد ملی", null=True,
    )  # کد ملی اضافه شد

    def __str__(self):
        return self.username

class DynamicColumn(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام ستون")
    data_type = models.CharField(
        max_length=50,
        choices=[
            ('char', 'متن'),
            ('int', 'عدد'),
            ('date', 'تاریخ'),
            ('bool', 'بولین'),
        ],
        verbose_name="نوع داده"
    )

    def __str__(self):
        return self.name

class Student(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    age = models.IntegerField(verbose_name="سن")
    major = models.CharField(max_length=100, verbose_name="رشته")
    father_job = models.CharField(max_length=100, verbose_name="شغل پدر")
    path = models.CharField(max_length=50, verbose_name="مسیر (آغاز/پرواز)")
    address = models.TextField(verbose_name="آدرس خانه")
    card_number = models.CharField(max_length=20, verbose_name="شماره کارت")
    national_code = models.CharField(max_length=10, verbose_name="کد ملی")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    birth_date = models.DateField(verbose_name="تاریخ تولد")
    Description = models.TextField(verbose_name="توضیحات", null=True)
    skill = models.TextField(verbose_name="مهارت ها", null=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    def get_dynamic_value(self, column):
        try:
            dynamic_value = self.dynamic_values.get(column=column)
            return dynamic_value.get_value()
        except DynamicValue.DoesNotExist:
            return None


class DynamicValue(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='dynamic_values')
    column = models.ForeignKey(DynamicColumn, on_delete=models.CASCADE)
    value_char = models.CharField(max_length=255, blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)
    value_bool = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.column.name}: {self.get_value()}"

    def get_value(self):
        if self.column.data_type == 'char':
            return self.value_char
        elif self.column.data_type == 'int':
            return self.value_int
        elif self.column.data_type == 'date':
            return self.value_date
        elif self.column.data_type == 'bool':
            return self.value_bool
        return None

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)  # متن استخراج‌شده
    # markdown_text = models.TextField(blank=True, null=True)  # متن مارک‌داون شده
    students = models.ManyToManyField(Student, related_name="uploaded_files", blank=True)

    def save(self, *args, **kwargs):
        if self.extracted_text:
            self.markdown_text = markdown.markdown(self.extracted_text)  # تبدیل به مارک‌داون
        super().save(*args, **kwargs)

    def __str__(self):
        return f"File: {self.file.name} - Uploaded at {self.uploaded_at}"


class SchoolClass(models.Model):
    class_name = models.CharField(max_length=100, verbose_name="نام کلاس")
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taught_classes',
        verbose_name="استاد"
    )
    students = models.ManyToManyField(
        Student,
        related_name='enrolled_classes',
        verbose_name="دانش‌آموزان"
    )
    teaching_assistants = models.ManyToManyField(
        CustomUser,
        related_name='assisted_classes',
        verbose_name="دستیاران آموزشی (تی‌ای‌ها)",
        blank=True
    )

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = "کلاس روبیکمپی"
        verbose_name_plural = "کلاس‌های روبیکمپ"


# python manage.py makemigrations
# python manage.py migrate


