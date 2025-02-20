من چنین کدی دارم که میاد دانش آموزان رو تو وکتور دیتابیس اد میکنه

```

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
                birth_date=gregorian_date
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
                f"تاریخ تولد: {gregorian_date}"
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


```

حالا می خوام وقتی تک دانش آموز هم همین طور در دیتابیس اد بشه

```
def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "دانش‌آموز با موفقیت اضافه شد!")
            return redirect('admin_dashboard')
    else:
        form = StudentForm()
    return render(
        request,
        'admin_panel/add_student.html',
        {'form': form}
    )
```

