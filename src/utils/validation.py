import re

def validate_student_id(student_id):
    return bool(re.match(r'^\d{8}$', student_id))

def validate_professor_id(professor_id):
    return bool(re.match(r'^\d{4}$', professor_id))

def validate_course_id(course_id):
    return bool(re.match(r'^[a-zA-Z0-9_\-]+$', course_id))

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    if len(password) < 8:
        return False, "رمز عبور باید حداقل 8 کاراکتر داشته باشد"
    if not any(char.isdigit() for char in password):
        return False, "رمز عبور باید حداقل یک عدد داشته باشد"
    if not any(char.isupper() for char in password):
        return False, "رمز عبور باید حداقل یک حرف بزرگ داشته باشد"
    if not any(char.islower() for char in password):
        return False, "رمز عبور باید حداقل یک حرف کوچک داشته باشد"
    return True, "رمز عبور معتبر است"
