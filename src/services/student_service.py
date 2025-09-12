import json
from config import THESIS_REQUESTS_FILE, DEFENSE_REQUESTS_FILE, COURSES_FILE, MIN_MONTHS_BEFORE_DEFENSE
from ..models.thesis_request import ThesisRequest
from ..models.defense_request import DefenseRequest
from ..services.auth_service import AuthService
from utils.date_utils import months_diff, get_current_date

class StudentService:
    def __init__(self, thesis_requests_file=THESIS_REQUESTS_FILE, 
                 defense_requests_file=DEFENSE_REQUESTS_FILE,
                 courses_file=COURSES_FILE):
        self.thesis_requests_file = thesis_requests_file
        self.defense_requests_file = defense_requests_file
        self.courses_file = courses_file
        self.auth_service = AuthService()
        self.thesis_requests = self.load_thesis_requests()
        self.defense_requests = self.load_defense_requests()
        self.courses = self.load_courses()
    
    def load_courses(self):
        try:
            with open(self.courses_file, 'r', encoding='utf-8') as file:
                courses_data = json.load(file)
                from ..models.course import Course
                return [Course.from_dict(data) for data in courses_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def save_courses(self):
        courses_data = [course.to_dict() for course in self.courses]
        with open(self.courses_file, 'w', encoding='utf-8') as file:
            json.dump(courses_data, file, ensure_ascii=False, indent=4)
    def request_thesis_course(self, student_id, course_id):
        try:
           
            for request in self.thesis_requests:
                if request.student_id == student_id and request.course_id == course_id:
                    return False, "شما قبلاً برای این درس درخواست داده‌اید"
            
            
            course = None
            course_index = -1
            for i, c in enumerate(self.courses):
                if c.course_id == course_id:
                    course = c
                    course_index = i
                    break
            
            if not course:
                return False, "درس مورد نظر یافت نشد"
            
            
            if not course.has_capacity():
                return False, "این درس ظرفیت ندارد"
            
            
            if not course.add_student():
                return False, "ظرفیت درس تکمیل است"
            
            
            new_request = ThesisRequest(
                student_id=student_id,
                course_id=course_id,
                professor_id=course.professor_id
            )
            
            self.thesis_requests.append(new_request)
            self.save_thesis_requests()
            self.save_courses() 
            
            return True, "درخواست با موفقیت ثبت شد و در انتظار تایید استاد است"
            
        except Exception as e:
            return False, f"خطا در ثبت درخواست: {str(e)}"
    def load_thesis_requests(self):
        try:
            with open(self.thesis_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
                return [ThesisRequest.from_dict(data) for data in requests_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def load_defense_requests(self):
        try:
            with open(self.defense_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
                return [DefenseRequest.from_dict(data) for data in requests_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def ourses(self):
        try:
            with open(self.courses_file, 'r', encoding='utf-8') as file:
                courses_data = json.load(file)
                return courses_data
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_thesis_requests(self):
        requests_data = [request.to_dict() for request in self.thesis_requests]
        with open(self.thesis_requests_file, 'w', encoding='utf-8') as file:
            json.dump(requests_data, file, ensure_ascii=False, indent=4)
    
    def save_defense_requests(self):
        requests_data = [request.to_dict() for request in self.defense_requests]
        with open(self.defense_requests_file, 'w', encoding='utf-8') as file:
            json.dump(requests_data, file, ensure_ascii=False, indent=4)
    
    def get_available_courses(self):
        
        try:
            available_courses = []
            for course in self.courses:
                if course.has_capacity():  
                    
                    professor = self.auth_service.get_user(course.professor_id)
                    course_data = {
                        "course_id": course.course_id,
                        "title": course.title,
                        "professor_id": course.professor_id,
                        "professor_name": professor.name if professor else "نامشخص",
                        "year": course.year,
                        "semester": course.semester,
                        "capacity": course.capacity,
                        "current_students": course.current_students,
                        "resources": course.resources,
                        "sessions": course.sessions,
                        "units": course.units
                    }
                    available_courses.append(course_data)
            return available_courses
        except Exception as e:
            print(f"Unexpected error processing course: {e}")
            return []
    def request_thesis_course(self, student_id, course_id):
        
        try:
            
            for request in self.thesis_requests:
                if request.student_id == student_id and request.course_id == course_id:
                    return False, "شما قبلاً برای این درس درخواست داده‌اید"
            
           
            course = None
            for c in self.courses:
                if c.course_id == course_id:
                    course = c
                    break
            
            if not course:
                return False, "درس مورد نظر یافت نشد"
            
            
            if not course.has_capacity():
                return False, "این درس ظرفیت ندارد"
            
           
            if not course.add_student():
                return False, "ظرفیت درس تکمیل است"
            
            
            new_request = ThesisRequest(
                student_id=student_id,
                course_id=course_id,
                professor_id=course.professor_id
            )
            
            self.thesis_requests.append(new_request)
            self.save_thesis_requests()
            self.save_courses() 
            
            return True, "درخواست با موفقیت ثبت شد و در انتظار تایید استاد است"
            
        except Exception as e:
            print(f"Unexpected error processing course: {e}")
            return False, f"خطا در ثبت درخواست: {str(e)}"
    def get_thesis_status(self, student_id):
       
        try:
            with open(self.thesis_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
            
            
            student_requests = []
            for data in requests_data:
                if str(data.get("student_id")) == str(student_id):
                    student_requests.append(data)
            
            return student_requests
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def can_request_defense(self, student_id):
       
        thesis_request = next((r for r in self.thesis_requests 
                              if r.student_id == student_id and r.status == "approved"), None)
        
        if not thesis_request:
            return False, "شما هیچ پایان‌نامه تأیید شده‌ای ندارید"
        
        
        if months_diff(thesis_request.approval_date, get_current_date()) < MIN_MONTHS_BEFORE_DEFENSE:
            return False, f"حداقل باید {MIN_MONTHS_BEFORE_DEFENSE} ماه از تأیید پایان‌نامه گذشته باشد"
        
        
        defense_request = next((r for r in self.defense_requests 
                               if r.student_id == student_id and r.status != "rejected"), None)
        
        if defense_request:
            status_map = {
                "pending": "درخواست دفاع شما در حال بررسی است",
                "approved": "درخواست دفاع شما تأیید شده است",
                "scheduled": "جلسه دفاع شما برنامه‌ریزی شده است",
                "completed": "دفاع شما انجام شده است"
            }
            return False, status_map.get(defense_request.status, "درخواست دفاع شما در حال پردازش است")
        
        return True, "می‌توانید درخواست دفاع دهید"
    
    def request_defense(self, student_id, thesis_data, pdf_file_path, first_page_img_path, last_page_img_path):
        
        can_request, message = self.can_request_defense(student_id)
        if not can_request:
            return False, message
        
        
        thesis_request = next((r for r in self.thesis_requests 
                              if r.student_id == student_id and r.status == "approved"), None)
        
       
        new_defense_request = DefenseRequest(
            student_id=student_id,
            professor_id=thesis_request.professor_id,
            thesis_title=thesis_data["title"],
            abstract=thesis_data["abstract"],
            keywords=thesis_data["keywords"],
            pdf_path=pdf_file_path,
            first_page_path=first_page_img_path,
            last_page_path=last_page_img_path
        )
        
        self.defense_requests.append(new_defense_request)
        self.save_defense_requests()
        return True, "درخواست دفاع با موفقیت ثبت شد و در انتظار تایید استاد است"
    
    def get_defense_status(self, student_id):
        defense_requests = [r for r in self.defense_requests if r.student_id == student_id]
        return defense_requests
