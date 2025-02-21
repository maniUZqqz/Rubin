import csv
from faker import Faker
import random

# ایجاد یک شیء Faker
fake = Faker()

# داده‌ها برای رشته‌های تحصیلی و مسیرها
majors = ['هوش مصنوعی', 'دیزاین', 'طراحی وبسایت', 'مارکتینگ']
paths = ['آغاز', 'پرواز']
father_jobs = ['معلم', 'کارمند بانک', 'راننده تاکسی', 'پزشک عمومی', 'مهندس عمران', 'باغدار', 'بازنشسته فرهنگی', 'کارمند شرکت خصوصی', 'فروشنده', 'آزاد']
# لیست توضیحات و مهارت‌ها
descriptions = ['مستعد در برنامه نویسی و شنا', 'علاقه‌مند به یادگیری زبان‌های جدید', 'فعال در ورزش‌های گروهی', 'دارای استعداد در ریاضی و حل مسائل پیچیده', 'علاقه‌مند به طراحی گرافیکی و هنر']
skills = ['Python', 'HTML/CSS', 'JavaScript', 'UI/UX Design', 'SEO', 'Marketing', 'Photoshop', 'English Language']

# سن ها بین 14 تا 18 سال
ages = list(range(14, 19))

# ایجاد 99 دانش‌آموز با داده‌های فیک
students = []
for _ in range(15):
    full_name = fake.name()  # نام و نام خانوادگی
    age = random.choice(ages)  # سن بین 14 تا 18 سال
    major = random.choice(majors)  # رشته تحصیلی از بین رشته‌های تعریف‌شده
    father_job = random.choice(father_jobs)  # شغل پدر از شغل‌های مختلف
    path = random.choice(paths)  # مسیر (آغاز یا پرواز)
    address = fake.address().replace('\n', ' ')  # آدرس
    card_number = fake.credit_card_number(card_type='mastercard')  # شماره کارت
    national_code = fake.unique.ssn()  # کد ملی به صورت SSN فیک
    postal_code = fake.zipcode()  # کد پستی
    birth_date = fake.date_of_birth(minimum_age=14, maximum_age=18)  # تاریخ تولد
    email = fake.email()  # ایمیل
    description = random.choice(descriptions)  # انتخاب توضیحات تصادفی
    skill = random.choice(skills)  # انتخاب مهارت تصادفی

    # ساخت یک رکورد برای دانش‌آموز
    student = {
        'نام و نام خانوادگی': full_name,
        'سن': age,
        'رشته': major,
        'شغل پدر': father_job,
        'مسیر (آغاز/پرواز)': path,
        'آدرس خانه': address,
        'شماره کارت': card_number,
        'کد ملی': national_code,
        'کد پستی': postal_code,
        'تاریخ تولد': birth_date.strftime('%Y/%m/%d'),  # فرمت تاریخ به شکل yyyy/mm/dd
        'توضیحات': description,  # توضیحات
        'مهارت ها': skill,  # مهارت‌ها
        'ایمیل': email  # ایمیل
    }

    students.append(student)

# نوشتن داده‌ها در یک فایل CSV
csv_file = 'students.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = [
        'نام و نام خانوادگی', 'سن', 'رشته', 'شغل پدر', 'مسیر (آغاز/پرواز)',
        'آدرس خانه', 'شماره کارت', 'کد ملی', 'کد پستی', 'تاریخ تولد',
        'توضیحات', 'مهارت ها', 'ایمیل'
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # نوشتن هدر فایل CSV
    writer.writerows(students)  # نوشتن داده‌های دانش‌آموزان

print(f"{len(students)} دانش‌آموز به فایل CSV اضافه شد.")
