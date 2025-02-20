# views.py
import csv
import random
import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    ForgotPasswordForm,
    OTPVerificationForm,
    ResetPasswordForm,
    FileUploadForm,
    DynamicValueForm
)
from .models import CustomUser, UploadedFile, Student
import markdown
import jdatetime
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student, DynamicColumn, DynamicValue
from .models import DynamicColumn
from .models import SchoolClass
from .forms import SchoolClassForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from .tasks import process_file_task
from pinecone import Pinecone, ServerlessSpec

# تنظیمات API
# تنظیمات OpenAI
client = OpenAI(
    base_url="https://api.avalai.ir/v1",
    api_key="aa-7Wb3vINvlb995eXrLJtsYl5lHoFlUk9j9Zj7j4MQviGhsZNt"
)



def chat_with_ai(request):
    if request.method == 'POST':
        try:
            # دریافت سوال از کاربر
            question = request.POST.get('question')

            # دریافت تاریخچه چت از `session`
            conversation_history = request.session.get('conversation_history', [])

            # دریافت تمام دانش‌آموزان از دیتابیس
            students = Student.objects.all()

            # ساخت context با اطلاعات دانش‌آموزان
            context = "\n".join([
                f"{student.full_name}: "
                f"سن: {student.age}, "
                f"رشته: {student.major}, "
                f"وضعیت در روبیکمپ: {student.path}, "
                f"شغل پدر: {student.father_job}, "
                f"آدرس: {student.address}, "
                f"کد ملی: {student.national_code}, "
                f"کد پستی: {student.postal_code}, "
                f"تاریخ تولد: {student.birth_date}, "
                f"توضیحات: {student.Description}, "
                f"مهارت ها: {student.skill}"
                for student in students
            ])

            # آماده‌سازی پرامپت برای مدل
            system_prompt = f"""
            شما یک دستیار هوشمند هستید که فقط بر اساس متن زیر به سوالات پاسخ می‌دهید:
            متن:
            {context}

            - اگر جواب در متن وجود نداشت، فقط بنویسید: "جواب پیدا نشد".
            - خارج از متن نظری ندید.
            - پاسخ‌ها کوتاه و دقیق باشند.
            """

            # افزودن سیستم پرامپت به تاریخچه (در صورتی که اولین پیام باشد)
            if not conversation_history:
                conversation_history.append({"role": "system", "content": system_prompt})

            # افزودن سوال کاربر به تاریخچه
            conversation_history.append({"role": "user", "content": question})

            # ارسال درخواست به هوش مصنوعی
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history
            )

            # دریافت پاسخ از هوش مصنوعی
            answer = response.choices[0].message.content.strip()

            # افزودن پاسخ به تاریخچه
            conversation_history.append({"role": "assistant", "content": answer})

            # ذخیره تاریخچه در `session`
            request.session['conversation_history'] = conversation_history

            return render(request, 'admin_panel/AI-Chat.html', {
                'conversation_history': conversation_history
            })

        except Exception as e:
            return render(request, 'admin_panel/AI-Chat.html', {
                'error': str(e)
            })

    # نمایش صفحه همراه با تاریخچه چت در `session`
    return render(request, 'admin_panel/AI-Chat.html', {
        'conversation_history': request.session.get('conversation_history', [])
    })


def reset_chat(request):
    request.session['conversation_history'] = []
    return redirect('chat_with_ai')


def add_dynamic_column(request):
    if request.method == 'POST':
        column_name = request.POST.get('column_name')
        data_type = request.POST.get('data_type')
        if column_name and data_type:
            DynamicColumn.objects.create(name=column_name, data_type=data_type)
            messages.success(request, "ستون با موفقیت اضافه شد!")
            return redirect('admin_dashboard')
    return render(request, 'admin_panel/add_column.html')


# ثبت‌نام کاربر
def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "ثبت‌نام موفق بود! خوش آمدید 😊")
        return redirect("profile")

    return render(request, "account/register.html", {"form": form})


# خروج از حساب کاربری
def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید!")
    return redirect("login")


# ورود به حساب کاربری
class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "ورود موفقیت‌آمیز بود!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "نام کاربری یا رمز عبور اشتباه است!")
        return super().form_invalid(form)


# صفحه پروفایل کاربر
@login_required
def profile_view(request):
    files = UploadedFile.objects.all()
    form = FileUploadForm()

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            process_file(uploaded_file.file.path, uploaded_file)
            messages.success(request, "فایل با موفقیت آپلود و پردازش شد!")
            return redirect('profile')

    return render(
        request,
        "account/profile.html",
        {"user": request.user, "files": files, "form": form}
    )


# @login_required
# def profile_view(request):
#     files = UploadedFile.objects.all()
#     form = FileUploadForm()
#
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = form.save()  # فایل ذخیره می‌شود
#             uploaded_file.refresh_from_db()  # اطمینان از ذخیره‌سازی فایل
#
#             print(f"Uploaded file path: {uploaded_file.file.path}, ID: {uploaded_file.id}")  # لاگ برای دیباگ
#
#             process_file_task.delay(uploaded_file.file.path, uploaded_file.id)  # ارسال به Celery
#
#             messages.success(request, "فایل با موفقیت آپلود شد و در حال پردازش است!")
#             return redirect('profile')  # ریدایرکت به صفحه پروفایل
#
#     return render(
#         request,
#         "account/profile.html",
#         {"user": request.user, "files": files, "form": form}
#     )


@login_required
def edit_profile_view(request):
    form = CustomUserCreationForm(request.POST or None, instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "پروفایل با موفقیت بروزرسانی شد!")
        return redirect("profile")

    return render(request, "account/edit_profile.html", {"form": form})


# بازیابی رمز عبور
def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        user = CustomUser.objects.filter(email=email).first()

        if user:
            otp_code = str(random.randint(100000, 999999))
            user.otp_code = otp_code
            user.save()
            send_mail("کد بازیابی رمز عبور", f"کد شما: {otp_code}", "noreply@yourdomain.com", [email])
            messages.success(request, "کد بازیابی ارسال شد!")
            return redirect("verify_otp")
        else:
            messages.error(request, "ایمیل یافت نشد!")

    return render(request, "account/forgot_password.html", {"form": form})


# تایید کد OTP
def verify_otp_view(request):
    form = OTPVerificationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        otp_code = form.cleaned_data["otp"]
        user = CustomUser.objects.filter(otp_code=otp_code).first()

        if user:
            messages.success(request, "کد تایید شد! رمز جدید را تنظیم کنید.")
            return redirect("reset_password", email=user.email)
        else:
            messages.error(request, "کد اشتباه است!")

    return render(request, "account/verify_otp.html", {"form": form})


# تغییر رمز عبور
def reset_password_view(request, email):
    form = ResetPasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        new_password = form.cleaned_data["new_password"]
        confirm_password = form.cleaned_data["confirm_password"]

        if new_password != confirm_password:
            messages.error(request, "رمزها مطابقت ندارند!")
            return redirect("reset_password", email=email)

        user = CustomUser.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)
            user.save()
            messages.success(request, "رمز عبور تغییر کرد!")
            return redirect("login")

    return render(request, "account/reset_password.html", {"form": form})


# پنل مدیریت (فقط برای سوپر یوزرها)
def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def admin_dashboard(request):
    files = UploadedFile.objects.all()
    students = Student.objects.all()  # دریافت تمام دانش‌آموزان
    dynamic_columns = DynamicColumn.objects.all()  # دریافت ستون‌های دینامیک
    school_classes = SchoolClass.objects.all()
    context = {
        "total_users": CustomUser.objects.count(),
        "flight_students": CustomUser.objects.filter(user_type="flight_student").count(),
        "beginner_students": CustomUser.objects.filter(user_type="beginner_student").count(),
        "files": files,  # اضافه کردن فایل‌ها به context
        "students": students,
        "dynamic_columns": dynamic_columns,  # ارسال ستون‌های دینامیک به تمپلیت
        "school_classes": school_classes,
    }
    return render(request, "admin_panel/dashboard.html", context)


def student_detail_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # چت بات هوش مصنوعی مخصوص این دانش‌آموز
    if request.method == 'POST':
        try:
            question = request.POST.get('question')
            conversation_history = request.session.get(f'conversation_history_{student_id}', [])

            # ساخت context با اطلاعات دانش‌آموز
            context = (
                f"{student.full_name}: "
                f"سن: {student.age}, "
                f"رشته: {student.major}, "
                f"وضعیت در روبیکمپ: {student.path}, "
                f"شغل پدر: {student.father_job}, "
                f"آدرس: {student.address}, "
                f"کد ملی: {student.national_code}, "
                f"کد پستی: {student.postal_code}, "
                f"تاریخ تولد: {student.birth_date}, "
                f"توضیحات: {student.Description}, "
                f"مهارت ها: {student.skill}"
            )

            system_prompt = f"""
            شما یک دستیار هوشمند هستید که فقط بر اساس متن زیر به سوالات پاسخ می‌دهید:
            متن:
            {context}

            - اگر جواب در متن وجود نداشت، فقط بنویسید: "جواب پیدا نشد".
            - خارج از متن نظری ندید.
            - پاسخ‌ها کوتاه و دقیق باشند.
            """

            if not conversation_history:
                conversation_history.append({"role": "system", "content": system_prompt})

            conversation_history.append({"role": "user", "content": question})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history
            )

            answer = response.choices[0].message.content.strip()
            conversation_history.append({"role": "assistant", "content": answer})

            request.session[f'conversation_history_{student_id}'] = conversation_history

            return render(request, 'admin_panel/student_detail.html', {
                'student': student,
                'conversation_history': conversation_history
            })

        except Exception as e:
            return render(request, 'admin_panel/student_detail.html', {
                'student': student,
                'error': str(e)
            })

    return render(request, 'admin_panel/student_detail.html', {
        'student': student,
        'conversation_history': request.session.get(f'conversation_history_{student_id}', [])
    })

# def process_file(file_path, uploaded_file):
#     if file_path.endswith('.csv'):
#         df = pd.read_csv(file_path)
#     elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
#         df = pd.read_excel(file_path)
#     students = []
#     for index, row in df.iterrows():
#         # تبدیل تاریخ شمسی به میلادی
#         jalali_date = row['تاریخ تولد']
#         year, month, day = map(int, jalali_date.split('/'))
#         gregorian_date = jdatetime.date(year, month, day).togregorian()
#
#         # ایجاد یا به‌روزرسانی کاربر
#         email = row.get('ایمیل', None)
#         username = row['نام و نام خانوادگی']  # نام کاربری همان نام کامل است
#         national_code = str(row['کد ملی'])  # کد ملی به عنوان رمز عبور استفاده می‌شود (تبدیل به رشته)
#
#         user, created = CustomUser.objects.get_or_create(
#             username=username,
#             defaults={
#                 'email': email,
#                 'national_code': national_code,
#                 'user_type': 'visitor',  # یا نوع کاربر مناسب
#             }
#         )
#         if created:
#             user.set_password(national_code)  # رمز عبور همان کد ملی است (به صورت رشته)
#             user.save()
#
#         # ایجاد دانش‌آموز
#         student = Student(
#             full_name=row['نام و نام خانوادگی'],
#             age=row['سن'],
#             major=row['رشته'],
#             father_job=row['شغل پدر'],
#             path=row['مسیر (آغاز/پرواز)'],
#             address=row['آدرس خانه'],
#             card_number=row['شماره کارت'],
#             national_code=national_code,  # کد ملی به صورت رشته
#             postal_code=row['کد پستی'],
#             birth_date=gregorian_date
#         )
#         student.save()
#         students.append(student)
#
#     uploaded_file.students.set(students)
#     uploaded_file.save()
#     return df.to_html(index=False)

# تنظیمات Pinecone

PINECONE_API_KEY = "pcsk_3JQw7_Jui1bJfxhxoPamQ7JseTpXzTBKHWka761AXJUtzML9opT9uTtoBPcmPNAE1uN8Q"
INDEX_NAME = "rubin"  # نام اندکس Pinecone
VECTOR_DIMENSION = 1536  # تعداد ابعاد امبدینگ مدل



# ایجاد نمونه Pinecone
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
except Exception as e:
    print(f"Error initializing Pinecone: {e}")
    raise

# بررسی اینکه آیا اندکس ایجاد شده یا خیر
try:
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=VECTOR_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
except Exception as e:
    print(f"Error creating Pinecone index: {e}")
    raise

# دسترسی به اندکس
try:
    index = pc.Index(INDEX_NAME)
except Exception as e:
    print(f"Error accessing Pinecone index: {e}")
    raise


def generate_embedding(text):
    """تولید امبدینگ برای متن داده شده"""
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise


def save_to_pinecone(vector_id, embedding, metadata):
    """ذخیره‌سازی امبدینگ در Pinecone"""
    try:
        vectors = [
            {
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            }
        ]
        index.upsert(vectors)
        print(f"Vector with ID '{vector_id}' added to Pinecone.")
    except Exception as e:
        print(f"Error saving to Pinecone: {e}")
        raise


def process_file(file_path, uploaded_file):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)

    students = []
    for index, row in df.iterrows():
        try:
            # تبدیل تاریخ شمسی به میلادی
            jalali_date = row['تاریخ تولد']
            year, month, day = map(int, jalali_date.split('/'))
            gregorian_date = jdatetime.date(year, month, day).togregorian()

            # ایجاد یا به‌روزرسانی کاربر
            email = row.get('ایمیل', None)
            username = row['نام و نام خانوادگی']  # نام کاربری همان نام کامل است
            national_code = str(row['کد ملی'])  # کد ملی به عنوان رمز عبور استفاده می‌شود (تبدیل به رشته)

            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'national_code': national_code,
                    'user_type': 'visitor',  # یا نوع کاربر مناسب
                }
            )
            if created:
                user.set_password(national_code)  # رمز عبور همان کد ملی است (به صورت رشته)
                user.save()

            # ایجاد دانش‌آموز
            student = Student(
                full_name=row['نام و نام خانوادگی'],
                age=row['سن'],
                major=row['رشته'],
                father_job=row['شغل پدر'],
                path=row['مسیر (آغاز/پرواز)'],
                address=row['آدرس خانه'],
                card_number=row['شماره کارت'],
                national_code=national_code,  # کد ملی به صورت رشته
                postal_code=row['کد پستی'],
                birth_date=gregorian_date,
                Description=row.get('توضیحات', None),  # توضیحات
                skill=row.get('مهارت ها', None),  # مهارت‌ها
                email=row.get('ایمیل', None),  # ایمیل
            )
            student.save()
            students.append(student)

            # ترکیب اطلاعات دانش‌آموز در یک رشته
            student_info = (
                f"نام و نام خانوادگی: {row['نام و نام خانوادگی']}, "
                f"سن: {row['سن']}, "
                f"رشته: {row['رشته']}, "
                f"شغل پدر: {row['شغل پدر']}, "
                f"مسیر: {row['مسیر (آغاز/پرواز)']}, "
                f"آدرس: {row['آدرس خانه']}, "
                f"کد ملی: {national_code}, "
                f"کد پستی: {row['کد پستی']}, "
                f"تاریخ تولد: {gregorian_date}, "
                f"توضیحات: {row.get('توضیحات', '')}, "
                f"مهارت‌ها: {row.get('مهارت ها', '')}, "
                f"ایمیل: {email}"
            )

            # تولید امبدینگ برای اطلاعات دانش‌آموز
            embedding = generate_embedding(student_info)

            # ذخیره‌سازی در Pinecone
            vector_id = f"student_{student.id}"  # آیدی منحصر به‌فرد برای بردار
            metadata = {
                "full_name": row['نام و نام خانوادگی'],
                "national_code": national_code,
                "birth_date": gregorian_date.strftime("%Y-%m-%d")
            }
            save_to_pinecone(vector_id, embedding, metadata)

        except Exception as e:
            print(f"Error processing student {row['نام و نام خانوادگی']}: {e}")
            continue

    uploaded_file.students.set(students)
    uploaded_file.save()
    return df.to_html(index=False)




def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()  # ذخیره دانش‌آموز در دیتابیس اصلی
            messages.success(request, "دانش‌آموز با موفقیت اضافه شد!")

            # ترکیب اطلاعات دانش‌آموز در یک رشته
            student_info = (
                f"نام و نام خانوادگی: {student.full_name}, "
                f"سن: {student.age}, "
                f"رشته: {student.major}, "
                f"شغل پدر: {student.father_job}, "
                f"مسیر: {student.path}, "
                f"آدرس: {student.address}, "
                f"کد ملی: {student.national_code}, "
                f"کد پستی: {student.postal_code}, "
                f"تاریخ تولد: {student.birth_date}"
            )

            # تولید امبدینگ برای اطلاعات دانش‌آموز
            embedding = generate_embedding(student_info)

            # ذخیره‌سازی در Pinecone
            vector_id = f"student_{student.id}"  # آیدی منحصر به‌فرد برای بردار
            metadata = {
                "full_name": student.full_name,
                "national_code": student.national_code,
                "birth_date": student.birth_date.strftime("%Y-%m-%d")
            }
            save_to_pinecone(vector_id, embedding, metadata)

            # اضافه کردن کاربر به لیست کاربران (CustomUser)
            email = student.email  # فرض می‌کنیم ایمیل دانش‌آموز از فرم گرفته شده است
            national_code = student.national_code
            username = student.full_name  # نام کاربری همان نام کامل است

            # ایجاد یا به‌روزرسانی کاربر
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'national_code': national_code,
                    'user_type': 'student',  # نوع کاربر به‌طور پیش‌فرض 'student' است
                }
            )
            if created:
                user.set_password(national_code)  # رمز عبور همان کد ملی است (به صورت رشته)
                user.save()

            return redirect('admin_dashboard')
    else:
        form = StudentForm()
    return render(
        request,
        'admin_panel/add_student.html',
        {'form': form}
    )



@login_required
def edit_student_view(request, student_id):
    try:
        student = Student.objects.get(id=student_id)  # پیدا کردن دانش‌آموز از طریق آیدی
    except Student.DoesNotExist:
        messages.error(request, "دانش‌آموز مورد نظر یافت نشد.")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)  # فرم برای ویرایش اطلاعات دانش‌آموز

        if form.is_valid():
            # ذخیره تغییرات در دیتابیس
            student = form.save()  # ذخیره اطلاعات ویرایش‌شده دانش‌آموز

            # ترکیب اطلاعات جدید دانش‌آموز در یک رشته
            student_info = (
                f"نام و نام خانوادگی: {student.full_name}, "
                f"سن: {student.age}, "
                f"رشته: {student.major}, "
                f"شغل پدر: {student.father_job}, "
                f"مسیر: {student.path}, "
                f"آدرس: {student.address}, "
                f"کد ملی: {student.national_code}, "
                f"کد پستی: {student.postal_code}, "
                f"تاریخ تولد: {student.birth_date}, "
                f"توضیحات: {student.Description}, "
                f"مهارت‌ها: {student.skill}, "
                f"ایمیل: {student.email}"
            )

            # تولید امبدینگ برای اطلاعات ویرایش‌شده
            embedding = generate_embedding(student_info)

            # به‌روزرسانی وکتور در Pinecone
            vector_id = f"student_{student.id}"  # آیدی منحصر به‌فرد برای وکتور
            metadata = {
                "full_name": student.full_name,
                "national_code": student.national_code,
                "birth_date": student.birth_date.strftime("%Y-%m-%d")
            }

            # ذخیره‌سازی وکتور جدید در Pinecone (آپدیت یا افزودن)
            save_to_pinecone(vector_id, embedding, metadata)

            messages.success(request, "پروفایل دانش‌آموز با موفقیت بروزرسانی شد!")
            return redirect('admin_dashboard')  # هدایت به داشبورد ادمین یا هر صفحه دلخواه

    else:
        form = StudentForm(instance=student)  # فرم با داده‌های موجود برای ویرایش

    return render(request, 'admin_panel/edit_student.html', {'form': form, 'student': student})


def check_vector_in_pinecone(vector_id):
    try:
        result = index.fetch([vector_id])
        if result and vector_id in result:
            print(f"Vector with ID '{vector_id}' exists in Pinecone.")
        else:
            print(f"Vector with ID '{vector_id}' does not exist in Pinecone.")
    except Exception as e:
        print(f"Error checking vector in Pinecone: {e}")



def delete_student_view(request, student_id):
    student = Student.objects.get(id=student_id)
    student.delete()
    messages.success(request, "دانش‌آموز با موفقیت حذف شد!")
    return redirect('admin_dashboard')


def add_school_class(request):
    if request.method == 'POST':
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "کلاس با موفقیت اضافه شد!")
            return redirect('admin_dashboard')
    else:
        form = SchoolClassForm()
    return render(request, 'admin_panel/add_school_class.html', {'form': form})


def edit_school_class(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    if request.method == 'POST':
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            messages.success(request, "کلاس با موفقیت بروزرسانی شد!")
            return redirect('admin_dashboard')
    else:
        form = SchoolClassForm(instance=school_class)
    return render(request, 'admin_panel/edit_school_class.html', {'form': form, 'school_class': school_class})


def delete_school_class(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    school_class.delete()
    messages.success(request, "کلاس با موفقیت حذف شد!")
    return redirect('admin_dashboard')
