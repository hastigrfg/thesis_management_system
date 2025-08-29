import os
import json
from src.services.auth_service import AuthService
from src.services.student_service import StudentService
from src.services.professor_service import ProfessorService
from src.services.evaluator_service import EvaluatorService
from src.services.search_service import SearchService
from src.utils.file_handler import save_thesis_file, save_image_file
from src.utils.validation import validate_password

class ThesisManagementSystem:
    def __init__(self):
        self.auth_service = AuthService()
        self.student_service = StudentService()
        self.professor_service = ProfessorService()
        self.evaluator_service = EvaluatorService()
        self.search_service = SearchService()
        self.current_user = None
    
    def run(self):
        while True:
            if not self.current_user:
                self.show_login_menu()
            else:
                if self.current_user.get_role() == "student":
                    self.show_student_menu()
                elif self.current_user.get_role() == "professor":
                    self.show_professor_menu()
    
    def show_login_menu(self):
        print("\n" + "="*50)
        print("سامانه مدیریت پایان‌نامه‌ها")
        print("="*50)
        print("1. ورود به سیستم")
        print("2. خروج")
        
        choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
        
        if choice == "1":
            self.login()
        elif choice == "2":
            print("خروج از سیستم...")
            exit()
        else:
            print("گزینه نامعتبر!")
    
    def login(self):
        user_id = input("کد کاربری: ")
        password = input("رمز عبور: ")
        
        user = self.auth_service.login(user_id, password)
        if user:
            self.current_user = user
            print(f"خوش آمدید {user.name}!")
            
            # بررسی نقش کاربر
            if user.get_role() == "external_evaluator":
                self.show_evaluator_menu()
                return
            elif user.get_role() == "professor":
                self.show_professor_menu()
                return
            elif user.get_role() == "student":
                self.show_student_menu()
                return
                
        else:
            print("کد کاربری یا رمز عبور اشتباه است!")
            
    def show_student_menu(self):
        while True:
            print("\n" + "="*50)
            print("منوی دانشجو")
            print("="*50)
            print("1. درخواست اخذ درس پایان‌نامه")
            print("2. مشاهده وضعیت درخواست‌ها")
            print("3. درخواست دفاع")
            print("4. جستجو در بانک پایان‌نامه‌ها")
            print("5. تغییر رمز عبور")
            print("6. خروج از حساب کاربری")
            
            choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
            
            if choice == "1":
                self.request_thesis_course()
            elif choice == "2":
                self.view_request_status()
            elif choice == "3":
                self.request_defense()
            elif choice == "4":
                self.search_theses()
            elif choice == "5":
                self.change_password()
            elif choice == "6":
                self.current_user = None
                print("با موفقیت خارج شدید.")
                break
            else:
                print("گزینه نامعتبر!")
    
    def show_professor_menu(self):
        """منوی استاد راهنما"""
        from services.evaluator_service import EvaluatorService
        
        evaluator_service = EvaluatorService()
        
        while True:
            print("\n" + "="*50)
            print("منوی استاد")
            print("="*50)
            print("1. مشاهده و بررسی درخواست‌های پایان‌نامه")
            print("2. مشاهده و بررسی درخواست‌های دفاع")
            print("3. تکمیل فرآیند دفاع")
            print("4. ثبت نمره به عنوان داور")  # گزینه جدید
            print("5. جستجو در بانک پایان‌نامه‌ها")
            print("6. تغییر رمز عبور")
            print("7. خروج از حساب کاربری")
            
            choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
            
            if choice == "1":
                self.review_thesis_requests()
            elif choice == "2":
                self.review_defense_requests()
            elif choice == "3":
                self.complete_defense()
            elif choice == "4":  # گزینه جدید
                self.evaluate_as_internal_evaluator(evaluator_service)
            elif choice == "5":
                self.search_theses()
            elif choice == "6":
                self.change_password()
            elif choice == "7":
                self.current_user = None
                print("با موفقیت خارج شدید.")
                break
            else:
                print("گزینه نامعتبر!")
    def request_thesis_course(self):
        available_courses = self.student_service.get_available_courses()
        
        if not available_courses:
            print("هیچ درس پایان‌نامه‌ای با ظرفیت خالی موجود نیست.")
            return
        
        print("\nدروس available:")
        for i, course in enumerate(available_courses, 1):
            print(f"{i}. {course['title']} - استاد: {course['professor_name']} - ظرفیت: {course['current_students']}/{course['capacity']}")
        
        try:
            course_choice = int(input("\nشماره درس مورد نظر را انتخاب کنید: ")) - 1
            if 0 <= course_choice < len(available_courses):
                course_id = available_courses[course_choice]['course_id']
                success, message = self.student_service.request_thesis_course(self.current_user.user_id, course_id)
                print(message)
            else:
                print("شماره درس نامعتبر!")
        except ValueError:
            print("لطفاً یک عدد وارد کنید!")
    
    def review_defense_requests(self):
        requests = self.professor_service.get_defense_requests(self.current_user.user_id)
        
        if not requests:
            print("هیچ درخواست دفاعی برای بررسی وجود ندارد.")
            return
        
        print("\nدرخواست‌های دفاع برای بررسی:")
        for i, request in enumerate(requests, 1):
            print(f"{i}. دانشجو: {request['student_id']} - عنوان: {request.get('thesis_title', 'بدون عنوان')}")  # تغییر این خط
        
        try:
            choice = int(input("\nشماره درخواست برای بررسی را انتخاب کنید: ")) - 1
            if 0 <= choice < len(requests):
                request = requests[choice]
                print(f"\nبررسی درخواست دفاع دانشجو {request['student_id']}")  # تغییر این خط
                print(f"عنوان: {request.get('thesis_title', 'بدون عنوان')}")  # تغییر این خط
                print(f"چکیده: {request.get('abstract', '')[:100]}...")  # تغییر این خط
                
                action = input("آیا می‌خواهید این درخواست را تأیید کنید؟ (y/n): ").lower()
                
                if action == 'y':
                    defense_date = input("تاریخ دفاع (YYYY-MM-DD): ")
                    internal_evaluator = input("کد داور داخلی: ")
                    external_evaluator = input("کد داور خارجی: ")
                    
                    success, message = self.professor_service.process_defense_request(
                        request['student_id'], self.current_user.user_id, True, defense_date, internal_evaluator, external_evaluator  # تغییر این خط
                    )
                    print(message)
                elif action == 'n':
                    reason = input("دلیل رد درخواست: ")
                    success, message = self.professor_service.process_defense_request(
                        request['student_id'], self.current_user.user_id, False, rejection_reason=reason  # تغییر این خط
                    )
                    print(message)
                else:
                    print("عملیات لغو شد.")
            else:
                print("شماره درخواست نامعتبر!")
        except ValueError:
            print("لطفاً یک عدد وارد کنید!")
    def request_defense(self):
        # بررسی امکان درخواست دفاع
        can_request, message = self.student_service.can_request_defense(self.current_user.user_id)
        if not can_request:
            print(message)
            return

        print("\nثبت درخواست دفاع")
        print("لطفاً اطلاعات پایان‌نامه خود را وارد کنید:")
        
        title = input("عنوان پایان‌نامه: ")
        abstract = input("چکیده: ")
        keywords = input("کلمات کلیدی (با کاما جدا کنید): ").split(',')

        print("\nلطفاً مسیر فایل‌های مورد نیاز را وارد کنید:")
        print("توجه: مسیر فایل نباید شامل کاراکترهای خاص مانند ! ' و غیره باشد")
        
        pdf_path = input("فایل PDF پایان‌نامه: ").strip('"')  # حذف کوتیشن اگر وجود دارد
        first_page_path = input("تصویر صفحه اول: ").strip('"')
        last_page_path = input("تصویر صفحه آخر: ").strip('"')

        # حذف کاراکترهای خاص از مسیرها
        pdf_path = pdf_path.replace('"', '').replace("'", "")
        first_page_path = first_page_path.replace('"', '').replace("'", "")
        last_page_path = last_page_path.replace('"', '').replace("'", "")

        # ذخیره فایل‌ها
        try:
            saved_pdf_path = save_thesis_file(pdf_path, self.current_user.user_id, os.path.basename(pdf_path))
            saved_first_page = save_image_file(first_page_path, self.current_user.user_id, "first_page", os.path.basename(first_page_path))
            saved_last_page = save_image_file(last_page_path, self.current_user.user_id, "last_page", os.path.basename(last_page_path))
            
            thesis_data = {
                "title": title,
                "abstract": abstract,
                "keywords": [k.strip() for k in keywords]
            }
            
            success, message = self.student_service.request_defense(
                self.current_user.user_id, thesis_data, saved_pdf_path, saved_first_page, saved_last_page
            )
            print(message)
            
        except Exception as e:
            print(f"خطا در ذخیره فایل‌ها: {e}")
            print("لطفاً مسیرهای ساده‌تر بدون کاراکترهای خاص استفاده کنید")
            
    def change_password(self):
        old_password = input("رمز عبور فعلی: ")
        new_password = input("رمز عبور جدید: ")
        confirm_password = input("تکرار رمز عبور جدید: ")
        
        if new_password != confirm_password:
            print("رمز عبور جدید و تکرار آن مطابقت ندارند.")
            return
        
        is_valid, message = validate_password(new_password)
        if not is_valid:
            print(message)
            return
        
        success = self.auth_service.change_password(self.current_user.user_id, old_password, new_password)
        if success:
            print("رمز عبور با موفقیت تغییر یافت.")
        else:
            print("تغییر رمز عبور ناموفق بود. لطفاً رمز عبور فعلی را صحیح وارد کنید.")
    
    def view_request_status(self):
        """مشاهده وضعیت درخواست‌های دانشجو"""
        requests = self.student_service.get_thesis_status(self.current_user.user_id)
        
        if not requests:
            print("هیچ درخواست پایان‌نامه‌ای ندارید.")
            return
        
        print("\nوضعیت درخواست‌های پایان‌نامه شما:")
        for i, request in enumerate(requests, 1):
            status_map = {
                "pending": "در انتظار تأیید استاد",
                "approved": "تأیید شده", 
                "rejected": "رد شده"
            }
            status = status_map.get(request.get("status", ""), "نامشخص")
            print(f"{i}. درس: {request.get('course_id', 'نامشخص')} - وضعیت: {status}")
            
            if request.get("status") == "rejected" and request.get("rejection_reason"):
                print(f"   دلیل رد: {request.get('rejection_reason')}")

    def review_thesis_requests(self):
        requests = self.professor_service.get_thesis_requests(self.current_user.user_id)
        
        if not requests:
            print("هیچ درخواست پایان‌نامه‌ای برای بررسی وجود ندارد.")
            return
        
        print("\nدرخواست‌های پایان‌نامه برای بررسی:")
        for i, request in enumerate(requests, 1):
            print(f"{i}. دانشجو: {request['student_id']} - درس: {request['course_id']}")
        
        try:
            choice = int(input("\nشماره درخواست برای بررسی را انتخاب کنید: ")) - 1
            if 0 <= choice < len(requests):
                request = requests[choice]
                print(f"\nبررسی درخواست دانشجو {request['student_id']} برای درس {request['course_id']}")
                
                action = input("آیا می‌خواهید این درخواست را تأیید کنید؟ (y/n): ").lower()
                
                if action == 'y':
                    success, message = self.professor_service.process_thesis_request(request['student_id'], self.current_user.user_id, True)
                    print(message)
                elif action == 'n':
                    reason = input("دلیل رد درخواست: ")
                    success, message = self.professor_service.process_thesis_request(request['student_id'], self.current_user.user_id, False, reason)
                    print(message)
                else:
                    print("عملیات لغو شد.")
            else:
                print("شماره درخواست نامعتبر!")
        except ValueError:
            print("لطفاً یک عدد وارد کنید!")
    
    def review_defense_requests(self):
        requests = self.professor_service.get_defense_requests(self.current_user.user_id)
        
        if not requests:
            print("هیچ درخواست دفاعی برای بررسی وجود ندارد.")
            return
        
        print("\nدرخواست‌های دفاع برای بررسی:")
        for i, request in enumerate(requests, 1):
            # این خط را تغییر دهید:
            print(f"{i}. دانشجو: {request['student_id']} - عنوان: {request.get('thesis_title', 'بدون عنوان')}")
        
        try:
            choice = int(input("\nشماره درخواست برای بررسی را انتخاب کنید: ")) - 1
            if 0 <= choice < len(requests):
                request = requests[choice]
                # این خطوط را تغییر دهید:
                print(f"\nبررسی درخواست دفاع دانشجو {request['student_id']}")
                print(f"عنوان: {request.get('thesis_title', 'بدون عنوان')}")
                print(f"چکیده: {request.get('abstract', '')[:100]}...")
                
                action = input("آیا می‌خواهید این درخواست را تأیید کنید؟ (y/n): ").lower()
                
                if action == 'y':
                    defense_date = input("تاریخ دفاع (YYYY-MM-DD): ")
                    internal_evaluator = input("کد داور داخلی: ")
                    external_evaluator = input("کد داور خارجی: ")
                    
                    # این خط را تغییر دهید:
                    success, message = self.professor_service.process_defense_request(
                        request['student_id'], self.current_user.user_id, True, defense_date, internal_evaluator, external_evaluator
                    )
                    print(message)
                elif action == 'n':
                    reason = input("دلیل رد درخواست: ")
                    # این خط را تغییر دهید:
                    success, message = self.professor_service.process_defense_request(
                        request['student_id'], self.current_user.user_id, False, rejection_reason=reason
                    )
                    print(message)
                else:
                    print("عملیات لغو شد.")
            else:
                print("شماره درخواست نامعتبر!")
        except ValueError:
            print("لطفاً یک عدد وارد کنید!")

    def complete_defense(self):
        scheduled_defenses = self.professor_service.get_scheduled_defenses(self.current_user.user_id)
        
        if not scheduled_defenses:
            print("هیچ جلسه دفاعی برای تکمیل وجود ندارد.")
            return
        
        print("\nجلسات دفاع برنامه‌ریزی شده:")
        for i, defense in enumerate(scheduled_defenses, 1):
            print(f"{i}. دانشجو: {defense['student_id']} - تاریخ: {defense.get('defense_date', 'بدون تاریخ')}")
        
        try:
            choice = int(input("\nشماره جلسه دفاع برای تکمیل را انتخاب کنید: ")) - 1
            if 0 <= choice < len(scheduled_defenses):
                defense = scheduled_defenses[choice]
                
                print(f"\nتکمیل جلسه دفاع دانشجو {defense['student_id']}")
                
                # فقط اطلاعات کلی را بگیر
                attendees = input("حاضرین جلسه (با کاما جدا کنید): ").split(',')
                defense_result = input("نتیجه دفاع (defended/redefense): ")
                
                # نمره استاد راهنما را جداگانه بگیر
                guidance_score = float(input("نمره استاد راهنما: "))
                
                success, message = self.professor_service.complete_defense_process(
                    defense['student_id'], guidance_score, None, None,
                    [a.strip() for a in attendees], defense_result
                )
                print(message)
            else:
                print("شماره جلسه دفاع نامعتبر!")
        except ValueError:
            print("لطفاً مقادیر عددی را صحیح وارد کنید!")
    def evaluate_as_internal_evaluator(self, evaluator_service):
            """ثبت نمره به عنوان داور داخلی"""
            theses_to_evaluate = evaluator_service.get_internal_theses_to_evaluate(self.current_user.user_id)
            
            if not theses_to_evaluate:
                print("هیچ پایان‌نامه‌ای برای ارزیابی به عنوان داور داخلی وجود ندارد.")
                return
            
            print("\nپایان‌نامه‌های برای ارزیابی (داور داخلی):")
            for i, thesis in enumerate(theses_to_evaluate, 1):
                print(f"{i}. دانشجو: {thesis['student_id']} - عنوان: {thesis.get('title', 'نامشخص')}")
            
            try:
                choice = int(input("\nشماره پایان‌نامه برای ارزیابی را انتخاب کنید: ")) - 1
                if 0 <= choice < len(theses_to_evaluate):
                    thesis = theses_to_evaluate[choice]
                    print(f"\nارزیابی پایان‌نامه دانشجو {thesis['student_id']}")
                    print(f"عنوان: {thesis.get('title', 'نامشخص')}")
                    print(f"نقش: داور داخلی")
                    
                    score = float(input("لطفاً نمره را وارد کنید (0-20): "))
                    
                    if score < 0 or score > 20:
                        print("نمره باید بین 0 تا 20 باشد.")
                        return
                    
                    success, message = evaluator_service.submit_internal_evaluation(
                        thesis['student_id'], self.current_user.user_id, score
                    )
                    print(message)
                else:
                    print("شماره پایان‌نامه نامعتبر!")
            except ValueError:
                print("لطفاً یک عدد وارد کنید!")

    def search_theses(self):
        """جستجو در بانک پایان‌نامه‌ها"""
        print("\nجستجو در بانک پایان‌نامه‌ها")
        print("لطفاً معیارهای جستجو را وارد کنید (در صورت عدم نیاز Enter بزنید):")
        
        query = input("عبارت جستجو: ") or None
        professor = input("کد استاد راهنما: ") or None
        keyword = input("کلمه کلیدی: ") or None
        author = input("کد دانشجویی نویسنده: ") or None
        year_input = input("سال دفاع: ") or None
        year = int(year_input) if year_input and year_input.isdigit() else None
        evaluator = input("کد داور: ") or None
        
        results = self.search_service.search_theses(query, professor, keyword, author, year, evaluator)
        
        if not results:
            print("هیچ پایان‌نامه‌ای با معیارهای جستجوی شما یافت نشد.")
            return
        
        print(f"\nتعداد نتایج یافت شده: {len(results)}")
        for i, thesis in enumerate(results, 1):
            print(f"\n{i}. عنوان: {thesis.get('title', 'نامشخص')}")
            print(f"   نویسنده: {thesis.get('student_id', 'نامشخص')}")
            print(f"   استاد راهنما: {thesis.get('professor_id', 'نامشخص')}")
            print(f"   سال: {thesis.get('year', 'نامشخص')}")
            print(f"   نمره نهایی: {thesis.get('final_score', 'ثبت نشده')}")
            
            # نمایش گرید
            final_score = thesis.get('final_score')
            if final_score is not None:
                if final_score >= 17:
                    grade = "الف"
                elif final_score >= 14:
                    grade = "ب"
                elif final_score >= 12:
                    grade = "ج"
                else:
                    grade = "د"
                print(f"   گرید: {grade}") 
    def show_evaluator_menu(self):
        """منوی داور خارجی"""
        from services.evaluator_service import EvaluatorService
        
        evaluator_service = EvaluatorService()
        
        while True:
            print("\n" + "="*50)
            print("منوی داور")
            print("="*50)
            print("1. ثبت نمره پایان‌نامه‌ها")
            print("2. جستجو در بانک پایان‌نامه‌ها")
            print("3. تغییر رمز عبور")
            print("4. خروج از حساب کاربری")  # تغییر نام گزینه
            
            choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
            
            if choice == "1":
                self.evaluate_theses(evaluator_service)
            elif choice == "2":
                self.search_theses()
            elif choice == "3":
                self.change_password()
            elif choice == "4":
                self.current_user = None
                print("با موفقیت خارج شدید.")
                break  # خارج شدن از حلقه و بازگشت به منوی اصلی
            else:
                print("گزینه نامعتبر!")
    def evaluate_theses(self, evaluator_service):
        """ثبت نمره توسط داور"""
        theses_to_evaluate = evaluator_service.get_theses_to_evaluate(self.current_user.user_id)
        
        if not theses_to_evaluate:
            print("هیچ پایان‌نامه‌ای برای ارزیابی وجود ندارد.")
            return
        
        print("\nپایان‌نامه‌های برای ارزیابی:")
        for i, thesis in enumerate(theses_to_evaluate, 1):
            print(f"{i}. دانشجو: {thesis['student_id']} - عنوان: {thesis.get('title', 'نامشخص')}")
        
        try:
            choice = int(input("\nشماره پایان‌نامه برای ارزیابی را انتخاب کنید: ")) - 1
            if 0 <= choice < len(theses_to_evaluate):
                thesis = theses_to_evaluate[choice]
                print(f"\nارزیابی پایان‌نامه دانشجو {thesis['student_id']}")
                print(f"عنوان: {thesis.get('title', 'نامشخص')}")
                
                score = float(input("لطفاً نمره را وارد کنید (0-20): "))
                
                if score < 0 or score > 20:
                    print("نمره باید بین 0 تا 20 باشد.")
                    return
                
                success, message = evaluator_service.submit_evaluation(
                    thesis['student_id'], self.current_user.user_id, score
                )
                print(message)
            else:
                print("شماره پایان‌نامه نامعتبر!")
        except ValueError:
            print("لطفاً یک عدد وارد کنید!")                
def main():
    system = ThesisManagementSystem()
    system.run()

if __name__ == "__main__":
    main()
