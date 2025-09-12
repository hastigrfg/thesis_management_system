import os

# مسیرهای پایه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARCHIVES_DIR = os.path.join(DATA_DIR, "archives")

# تنظیمات پایگاه داده
USERS_FILE = os.path.join(DATA_DIR, "users.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
THESIS_REQUESTS_FILE = os.path.join(DATA_DIR, "thesis_requests.json")
DEFENSE_REQUESTS_FILE = os.path.join(DATA_DIR, "defense_requests.json")
THESES_FILE = os.path.join(DATA_DIR, "theses.json")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")  # اضافه کردن این خط
MINUTES_FILE = os.path.join(DATA_DIR, "meeting_minutes.json")  # اضافه کردن این خط

# تنظیمات مسیرهای ذخیره‌سازی
THESES_DIR = os.path.join(ARCHIVES_DIR, "theses")
IMAGES_DIR = os.path.join(ARCHIVES_DIR, "images")

# تنظیمات سیستم
MIN_MONTHS_BEFORE_DEFENSE = 3
PROFESSOR_GUIDANCE_CAPACITY = 5
PROFESSOR_EVALUATION_CAPACITY = 10

EMAILS_FILE = os.path.join(DATA_DIR, "emails.json")
