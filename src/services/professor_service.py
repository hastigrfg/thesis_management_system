import json
from config import THESIS_REQUESTS_FILE, DEFENSE_REQUESTS_FILE, THESES_FILE
from ..models.thesis import Thesis
from ..services.auth_service import AuthService
from ..services.student_service import StudentService
from utils.date_utils import get_current_date

class ProfessorService:
    def __init__(self, thesis_requests_file=THESIS_REQUESTS_FILE, 
                 defense_requests_file=DEFENSE_REQUESTS_FILE,
                 theses_file=THESES_FILE):
        self.thesis_requests_file = thesis_requests_file
        self.defense_requests_file = defense_requests_file
        self.theses_file = theses_file
        self.auth_service = AuthService()
        self.student_service = StudentService()
    
    def get_thesis_requests(self, professor_id):
        """مستقیماً از فایل بخوانیم و فیلتر کنیم - راه مطمئن"""
        try:
            with open(self.thesis_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
                
            # فیلتر کردن درخواست‌های مربوط به استاد فعلی
            professor_requests = []
            for data in requests_data:
                if (str(data.get("professor_id")) == str(professor_id) and 
                    data.get("status") == "pending"):
                    professor_requests.append(data)
            
            return professor_requests
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_defense_requests(self, professor_id):
        """دریافت درخواست‌های دفاع مربوط به استاد"""
        try:
            with open(self.defense_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
                
            professor_requests = []
            for data in requests_data:
                if (str(data.get("professor_id")) == str(professor_id) and 
                    data.get("status") == "pending"):
                    professor_requests.append(data)
            
            return professor_requests
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def process_thesis_request(self, student_id, professor_id, approve, rejection_reason=None):
        """پردازش درخواست پایان‌نامه - نسخه ساده و مطمئن"""
        try:
            # خواندن همه درخواست‌ها
            with open(self.thesis_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
            
            # پیدا کردن درخواست
            request_index = -1
            for i, data in enumerate(requests_data):
                if (str(data.get("student_id")) == str(student_id) and 
                    str(data.get("professor_id")) == str(professor_id) and
                    data.get("status") == "pending"):
                    request_index = i
                    break
            
            if request_index == -1:
                return False, "درخواست یافت نشد"
            
            # بررسی ظرفیت استاد
            professor = self.auth_service.get_user(professor_id)
            if not professor:
                return False, "استاد راهنما یافت نشد"
            
            if approve:
                # بررسی ظرفیت
                if professor.current_guidance >= professor.capacity_guidance:
                    return False, "ظرفیت استاد راهنمایی تکمیل است"
                
                # تأیید درخواست
                requests_data[request_index]["status"] = "approved"
                requests_data[request_index]["approval_date"] = get_current_date().strftime("%Y-%m-%d %H:%M:%S")
                requests_data[request_index]["rejection_reason"] = None
                
                # افزایش ظرفیت استاد
                professor.current_guidance += 1
                message = "درخواست پایان‌نامه تأیید شد"
            else:
                # رد درخواست
                requests_data[request_index]["status"] = "rejected"
                requests_data[request_index]["approval_date"] = None
                requests_data[request_index]["rejection_reason"] = rejection_reason
                message = "درخواست پایان‌نامه رد شد"
            
            # ذخیره تغییرات
            with open(self.thesis_requests_file, 'w', encoding='utf-8') as file:
                json.dump(requests_data, file, ensure_ascii=False, indent=4)
            
            # ذخیره اطلاعات استاد
            self.auth_service.save_users()
            
            return True, message
            
        except Exception as e:
            return False, f"خطا در پردازش درخواست: {str(e)}"
    
    def process_defense_request(self, student_id, professor_id, approve, defense_date=None, 
                           internal_evaluator=None, external_evaluator=None, rejection_reason=None):
        """پردازش درخواست دفاع - نسخه ساده و مطمئن"""
        
        try:
            # بررسی که استاد راهنما نتواند داور باشد - اینجا اضافه شود
            if internal_evaluator == professor_id:
                return False, "استاد راهنما نمی‌تواند داور داخلی باشد"
            
            if external_evaluator == professor_id:
                return False, "استاد راهنما نمی‌تواند داور خارجی باشد"
            
            # خواندن همه درخواست‌ها
            with open(self.defense_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
            
            # پیدا کردن درخواست
            request_index = -1
            for i, data in enumerate(requests_data):
                if (str(data.get("student_id")) == str(student_id) and 
                    str(data.get("professor_id")) == str(professor_id) and
                    data.get("status") == "pending"):
                    request_index = i
                    break
            
            if request_index == -1:
                return False, "درخواست دفاع یافت نشد"
            
            if approve:
                if not defense_date or not internal_evaluator or not external_evaluator:
                    return False, "تاریخ دفاع و داوران باید مشخص شوند"
                
                # بررسی وجود داوران
                internal_prof = self.auth_service.get_user(internal_evaluator)
                external_prof = self.auth_service.get_user(external_evaluator)
                
                if not internal_prof:
                    return False, "داور داخلی یافت نشد"
                if not external_prof:
                    return False, "داور خارجی یافت نشد"
                
                # بررسی ظرفیت داوران
                if hasattr(internal_prof, 'can_accept_evaluation') and not internal_prof.can_accept_evaluation():
                    return False, "داور داخلی ظرفیت ندارد"
                if hasattr(external_prof, 'can_accept_evaluation') and not external_prof.can_accept_evaluation():
                    return False, "داور خارجی ظرفیت ندارد"
                
                # تأیید درخواست
                requests_data[request_index]["status"] = "scheduled"
                requests_data[request_index]["defense_date"] = defense_date
                requests_data[request_index]["internal_evaluator"] = internal_evaluator
                requests_data[request_index]["external_evaluator"] = external_evaluator
                requests_data[request_index]["rejection_reason"] = None
                
                # افزایش ظرفیت داوران (اگر متد exists دارد)
                if hasattr(internal_prof, 'add_evaluation'):
                    internal_prof.add_evaluation()
                if hasattr(external_prof, 'add_evaluation'):
                    external_prof.add_evaluation()
                    
                message = "درخواست دفاع تأیید و برنامه‌ریزی شد"
            else:
                # رد درخواست
                requests_data[request_index]["status"] = "rejected"
                requests_data[request_index]["defense_date"] = None
                requests_data[request_index]["internal_evaluator"] = None
                requests_data[request_index]["external_evaluator"] = None
                requests_data[request_index]["rejection_reason"] = rejection_reason
                message = "درخواست دفاع رد شد"
            
            # ذخیره تغییرات
            with open(self.defense_requests_file, 'w', encoding='utf-8') as file:
                json.dump(requests_data, file, ensure_ascii=False, indent=4)
            
            self.auth_service.save_users()
            return True, message
                
        except Exception as e:
            import traceback
            print(f"خطای کامل: {traceback.format_exc()}")
            return False, f"خطا در پردازش درخواست دفاع: {str(e)}"
    def get_scheduled_defenses(self, professor_id):
        """دریافت جلسات دفاع برنامه‌ریزی شده مربوط به استاد راهنما"""
        try:
            with open(self.defense_requests_file, 'r', encoding='utf-8') as file:
                requests_data = json.load(file)
            
            # فیلتر کردن جلسات دفاع scheduled مربوط به استاد راهنما
            scheduled_defenses = [
                data for data in requests_data 
                if data.get("status") == "scheduled" 
                and data.get("professor_id") == professor_id  # استاد راهنما
            ]
            
            return scheduled_defenses
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def complete_defense_process(self, student_id, guidance_score, internal_score, external_score, 
                            attendees, defense_result):
        try:
            # خواندن درخواست‌های دفاع
            with open(self.defense_requests_file, 'r', encoding='utf-8') as file:
                defense_requests = json.load(file)
            
            # ایجاد یا خواندن فایل theses.json
            try:
                with open(self.theses_file, 'r', encoding='utf-8') as file:
                    theses = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                theses = []  # اگر فایل وجود ندارد، لیست خالی ایجاد کن
            
            # پیدا کردن درخواست دفاع
            defense_index = -1
            for i, data in enumerate(defense_requests):
                if str(data.get("student_id")) == str(student_id) and data.get("status") == "scheduled":
                    defense_index = i
                    break
            
            if defense_index == -1:
                return False, "درخواست دفاع یافت نشد"
            
            defense_data = defense_requests[defense_index]
            
            # ایجاد رکورد پایان‌نامه
            thesis_data = {
                "student_id": defense_data["student_id"],
                "professor_id": defense_data["professor_id"],
                "title": defense_data["thesis_title"],
                "abstract": defense_data["abstract"],
                "keywords": defense_data["keywords"],
                "pdf_path": defense_data["pdf_path"],
                "first_page_path": defense_data["first_page_path"],
                "last_page_path": defense_data["last_page_path"],
                "year": get_current_date().year,
                "semester": "second" if get_current_date().month > 6 else "first",
                "defense_date": defense_data["defense_date"],
                "internal_evaluator": defense_data["internal_evaluator"],
                "external_evaluator": defense_data["external_evaluator"],
                "attendees": attendees,
                "guidance_score": guidance_score,
                "internal_score": internal_score,  # می‌تواند null باشد
                "external_score": external_score,  # می‌تواند null باشد
                "final_score": None,  # بعداً محاسبه می‌شود
                "defense_result": defense_result,
                "completion_date": get_current_date().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # اضافه کردن به لیست پایان‌نامه‌ها
            theses.append(thesis_data)
            
            # ذخیره در فایل
            with open(self.theses_file, 'w', encoding='utf-8') as file:
                json.dump(theses, file, ensure_ascii=False, indent=4)
            
            return True, "دفاع با موفقیت تکمیل و ثبت شد"
            
        except Exception as e:
            return False, f"خطا در تکمیل دفاع: {str(e)}"
