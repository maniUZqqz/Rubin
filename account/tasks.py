# from celery import shared_task
# from .models import UploadedFile
# from .views import process_file  # این تابع را چک کنید که درست کار می‌کند
#
# @shared_task
# def process_file_task(file_path, file_id):
#     try:
#         print(f"Received file_path: {file_path}, file_id: {file_id}")  # لاگ مقدار ورودی‌ها
#         uploaded_file = UploadedFile.objects.get(id=file_id)
#         process_file(file_path, uploaded_file)
#         return "File processed successfully!"
#     except Exception as e:
#         print(f"Error: {str(e)}")  # لاگ خطا
#         return f"Error: {str(e)}"
from celery import shared_task
from .models import UploadedFile

@shared_task
def process_file_task(file_path, file_id):
    try:
        from .views import process_file  # ایمپورت داخل تابع انجام شود
        uploaded_file = UploadedFile.objects.get(id=file_id)
        process_file(file_path, uploaded_file)
        return "File processed successfully!"
    except Exception as e:
        return f"Error: {str(e)}"
