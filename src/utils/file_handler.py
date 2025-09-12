import os
import shutil
import re
from datetime import datetime
from config import THESES_DIR, IMAGES_DIR

def ensure_directories():
    
    os.makedirs(THESES_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*\'!]', '', filename)
    return sanitized

def save_thesis_file(file_path, student_id, original_name):
    
    try:
        ensure_directories()
        
       
        safe_name = sanitize_filename(original_name)
        file_extension = os.path.splitext(safe_name)[1]
        
        
        new_filename = f"thesis_{student_id}_{int(datetime.now().timestamp())}{file_extension}"
        destination = os.path.join(THESES_DIR, new_filename)
        
        
        shutil.copy2(file_path, destination)
        return destination
        
    except Exception as e:
        print(f"خطا در ذخیره فایل پایان‌نامه: {e}")
        raise

def save_image_file(file_path, student_id, page_type, original_name):
    
    try:
        ensure_directories()
        
        
        safe_name = sanitize_filename(original_name)
        file_extension = os.path.splitext(safe_name)[1]
        
        
        new_filename = f"{page_type}_{student_id}_{int(datetime.now().timestamp())}{file_extension}"
        destination = os.path.join(IMAGES_DIR, new_filename)
        
       
        shutil.copy2(file_path, destination)
        return destination
        
    except Exception as e:
        print(f"خطا در ذخیره فایل تصویر: {e}")
        raise

def get_file_url(file_path):
   
    if not file_path or not os.path.exists(file_path):
        return None
    return file_path
