import os
import shutil
import re
from datetime import datetime
from config import THESES_DIR, IMAGES_DIR

def ensure_directories():
    """ایجاد پوشه‌های مورد نیاز در صورت عدم وجود"""
    os.makedirs(THESES_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

def sanitize_filename(filename):
    """حذف کاراکترهای غیرمجاز از نام فایل"""
    # حذف کاراکترهای غیرمجاز در نام فایل
    sanitized = re.sub(r'[<>:"/\\|?*\'!]', '', filename)
    return sanitized

def save_thesis_file(file_path, student_id, original_name):
    """ذخیره فایل پایان‌نامه"""
    try:
        ensure_directories()
        
        # تمیز کردن نام فایل
        safe_name = sanitize_filename(original_name)
        file_extension = os.path.splitext(safe_name)[1]
        
        # ایجاد نام فایل جدید
        new_filename = f"thesis_{student_id}_{int(datetime.now().timestamp())}{file_extension}"
        destination = os.path.join(THESES_DIR, new_filename)
        
        # کپی فایل
        shutil.copy2(file_path, destination)
        return destination
        
    except Exception as e:
        print(f"خطا در ذخیره فایل پایان‌نامه: {e}")
        raise

def save_image_file(file_path, student_id, page_type, original_name):
    """ذخیره فایل تصویر"""
    try:
        ensure_directories()
        
        # تمیز کردن نام فایل
        safe_name = sanitize_filename(original_name)
        file_extension = os.path.splitext(safe_name)[1]
        
        # ایجاد نام فایل جدید
        new_filename = f"{page_type}_{student_id}_{int(datetime.now().timestamp())}{file_extension}"
        destination = os.path.join(IMAGES_DIR, new_filename)
        
        # کپی فایل
        shutil.copy2(file_path, destination)
        return destination
        
    except Exception as e:
        print(f"خطا در ذخیره فایل تصویر: {e}")
        raise

def get_file_url(file_path):
    """دریافت آدرس فایل"""
    if not file_path or not os.path.exists(file_path):
        return None
    return file_path
