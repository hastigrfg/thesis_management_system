import os
import json
from src.services.auth_service import AuthService
from src.services.student_service import StudentService
from src.services.professor_service import ProfessorService
from src.services.evaluator_service import EvaluatorService
from src.services.search_service import SearchService
from src.utils.file_handler import save_thesis_file, save_image_file
from src.utils.validation import validate_password
from services.email_service import EmailService

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
            print("5. سیستم ایمیل")  
            print("6. داشبورد")
            print("7. تغییر رمز عبور")
            print("8. خروج از حساب کاربری")
                    
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
                self.email_menu()
            elif choice == "6":
                self.show_student_dashboard()
            elif choice == "7":
                self.change_password()
            elif choice == "8":
                self.current_user = None
                print("با موفقیت خارج شدید.")
                return
            else:
                print("گزینه نامعتبر!")
    
    def show_professor_menu(self):
        
        from src.services.evaluator_service import EvaluatorService
        
        evaluator_service = EvaluatorService()
        
        while True:
            print("\n" + "="*50)
            print("منوی استاد")
            print("="*50)
            print("1. مشاهده و بررسی درخواست‌های پایان‌نامه")
            print("2. مشاهده و بررسی درخواست‌های دفاع")
            print("3. تکمیل فرآیند دفاع")
            print("4. ثبت نمره پایان‌نامه (به عنوان داور داخلی)")  
            print("5. جستجو در بانک پایان‌نامه‌ها")
            print("6. سیستم ایمیل")
            print("7. داشبورد و گزارشات")
            print("8. ثبت صورت جلسه")
            print("9. تغییر رمز عبور")
            print("10. خروج از حساب کاربری")
                
            choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
                
            if choice == "1":
                self.review_thesis_requests()
            elif choice == "2":
                self.review_defense_requests()
            elif choice == "3":
                self.complete_defense()
            elif choice == "4":
                self.grade_as_internal_evaluator(evaluator_service)
            elif choice == "5":
                self.search_theses()
            elif choice == "6":
                self.email_menu()
            elif choice == "7":
                self.dashboard_menu()
            elif choice == "8":
                self.create_meeting_minutes()
            elif choice == "9":
                self.change_password()
            elif choice == "10":
                self.current_user = None
                print("با موفقیت خارج شدید.")
                return
            else:
                print("گزینه نامعتبر!")

    def grade_as_internal_evaluator(self, evaluator_service):
        
        print("\n--- ثبت نمره به عنوان داور داخلی ---")
        
        internal_evaluator_theses = evaluator_service.get_internal_theses_to_evaluate(self.current_user.user_id)
        
        if not internal_evaluator_theses:
            print("هیچ پایان‌نامه‌ای به عنوان داور داخلی ندارید.")
            return
        
        print("پایان‌نامه‌هایی که داور داخلی آنها هستید:")
        for i, thesis in enumerate(internal_evaluator_theses, 1):
           
            student_id = thesis.get('student_id')
            student = self.auth_service.get_user(student_id)
            student_name = student.name if student else "نامشخص"
            
            current_grade = thesis.get('internal_evaluator_grade', 'ثبت نشده')
            print(f"{i}. {thesis['title']} - دانشجو: {student_name} - نمره فعلی: {current_grade}")
        
        try:
            thesis_choice = int(input("شماره پایان‌نامه مورد نظر را انتخاب کنید: ")) - 1
            if thesis_choice < 0 or thesis_choice >= len(internal_evaluator_theses):
                print("شماره نامعتبر!")
                return
            
            selected_thesis = internal_evaluator_theses[thesis_choice]
            student_id = selected_thesis.get('student_id')
            
            
            grade = float(input("نمره پایان‌نامه (0-20): "))
            if grade < 0 or grade > 20:
                print("نمره باید بین 0 تا 20 باشد!")
                return
            
            
            success, message = evaluator_service.submit_internal_evaluation(
                student_id, self.current_user.user_id, grade
            )
            print(message)
                
        except ValueError:
            print("لطفاً عدد وارد کنید!")
        except Exception as e:
            print(f"خطا: {e}")
    def dashboard_menu(self):
        
        from services.dashboard_service import DashboardService
        from services.report_service import ReportService
        
        dashboard_service = DashboardService()
        report_service = ReportService()
        
        while True:
            print("\n📊 داشبورد و گزارشات")
            print("="*30)
            print("1. مشاهده داشبورد")
            print("2. گزارش عملکرد")
            print("3. آمار کلی")
            print("4. بازگشت به منوی اصلی")
            
            choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
            
            if choice == "1":
                self.show_professor_dashboard(dashboard_service)
            elif choice == "2":
                self.generate_report(report_service)
            elif choice == "3":
                self.show_statistics()
            elif choice == "4":
                break
            else:
                print("گزینه نامعتبر!")

    def show_professor_dashboard(self, dashboard_service):
       
        result = dashboard_service.get_professor_dashboard(self.current_user.user_id)
        
        if not result['success']:
            print(f"خطا: {result['message']}")
            return
        
        data = result
        print(f"\n📈 داشبورد استاد - {self.current_user.name}")
        print("="*50)
        print(f"👥 تعداد دانشجویان: {data['stats']['total_students']}")
        print(f"⏳ درخواست‌های در انتظار تأیید: {data['stats']['pending_approvals']}")
        print(f"📅 جلسات دفاع برنامه‌ریزی شده: {data['stats']['scheduled_defenses']}")
        print(f"✅ دفاع‌های تکمیل شده: {data['stats']['completed_defenses']}")
        print(f"📭 پیام‌های خوانده نشده: {data['stats']['unread_messages']}")
        
        if data['stats']['guidance_capacity']:
            cap = data['stats']['guidance_capacity']
            print(f"📊 ظرفیت راهنمایی: {cap['current']}/{cap['capacity']} (مانده: {cap['remaining']})")
        
        
        if data['pending_requests']:
            print(f"\n⏳ درخواست‌های در انتظار بررسی:")
            for req in data['pending_requests']:
                print(f"  • دانشجو: {req['student_id']} - درس: {req['course_id']}")
    def show_student_dashboard(self):
       
        from services.dashboard_service import DashboardService
        
        dashboard_service = DashboardService()
        result = dashboard_service.get_student_dashboard(self.current_user.user_id)
        
        if not result['success']:
            print(f"خطا: {result['message']}")
            return
        
        data = result
        print(f"\n📈 داشبورد دانشجو - {self.current_user.name}")
        print("="*50)
        print(f"📚 تعداد درخواست‌ها: {data['stats']['total_thesis_requests']}")
        print(f"✅ پایان‌نامه‌های تأیید شده: {data['stats']['approved_theses']}")
        print(f"⏳ درخواست‌های در انتظار: {data['stats']['pending_requests']}")
        print(f"🎓 درخواست‌های دفاع: {data['stats']['defense_requests']}")
        print(f"📭 پیام‌های خوانده نشده: {data['stats']['unread_messages']}")
        
        
        print(f"\n📅 آخرین فعالیت‌ها:")
        for activity in data['stats']['latest_activity'][:5]:  # ۵ فعالیت اخیر
            print(f"  • {activity['title']} - {activity['status']} - {activity['date']}")  
              
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
    def generate_report(self, report_service):
        
        if self.current_user.get_role() != "professor":
            print("این قابلیت فقط برای اساتید قابل دسترسی است.")
            return
        
        print("\n📄 گزارش عملکرد")
        print("="*30)
        
        start_date = input("تاریخ شروع (YYYY-MM-DD یا Enter برای همه): ")
        end_date = input("تاریخ پایان (YYYY-MM-DD یا Enter برای همه): ")
        
        result = report_service.generate_professor_report(
            self.current_user.user_id, 
            start_date if start_date else None, 
            end_date if end_date else None
        )
        
        if not result['success']:
            print(f"خطا: {result['message']}")
            return
        
        report = result['report']
        print(f"\n📋 گزارش عملکرد - {report['period']}")
        print("="*50)
        print(f"👥 تعداد دانشجویان: {report['total_students']}")
        print(f"🎓 پایان‌نامه‌های تکمیل شده: {report['completed_theses']}")
        print(f"📊 معدل نمرات: {report['average_score']}")
        print(f"✅ نرخ تأیید: {report['approval_rate']}%")
        
        print("\n📈 توزیع نمرات:")
        for grade, count in report['grade_distribution'].items():
            print(f"  {grade}: {count}")
        
        print(f"\n📅 آمار زمانی:")
        for year, count in report['timeline_data'].items():
            print(f"  {year}: {count} پایان‌نامه")
        
        input("\n↵ برای ادامه Enter بزنید")
    def show_statistics(self):
        
        from services.report_service import ReportService
        
        report_service = ReportService()
        
        
        result = report_service.generate_professor_report(self.current_user.user_id, None, None)
        
        if not result['success']:
            print(f"خطا: {result['message']}")
            return
        
        report = result['report']
        
        print(f"\n📊 آمار کلی عملکرد")
        print("="*40)
        print(f"👥 کل دانشجویان: {report['total_students']}")
        print(f"🎓 کل پایان‌نامه‌های تکمیل شده: {report['completed_theses']}")
        print(f"⭐ معدل نمرات: {report['average_score']}")
        print(f"📈 نرخ تأیید: {report['approval_rate']}%")
        
        print(f"\n🎯 توزیع نمرات:")
        for grade, count in report['grade_distribution'].items():
            percentage = (count / report['completed_theses'] * 100) if report['completed_theses'] > 0 else 0
            print(f"  {grade}: {count} ({percentage:.1f}%)")
        
        input("\n↵ برای ادامه Enter بزنید")
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
                print(f"\nبررسی درخواست دفاع دانشجو {request['student_id']}")  
                print(f"عنوان: {request.get('thesis_title', 'بدون عنوان')}")  
                print(f"چکیده: {request.get('abstract', '')[:100]}...") 
                
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
                        request['student_id'], self.current_user.user_id, False, rejection_reason=reason  
                    )
                    print(message)
                else:
                    print("عملیات لغو شد.")
            else:
                print("شماره درخواست نامعتبر!")
        except ValueError:
            print("لطفاً یک عدد وارد کنید!")
    def request_defense(self):
        
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
        
        pdf_path = input("فایل PDF پایان‌نامه: ").strip('"')  
        first_page_path = input("تصویر صفحه اول: ").strip('"')
        last_page_path = input("تصویر صفحه آخر: ").strip('"')

        
        pdf_path = pdf_path.replace('"', '').replace("'", "")
        first_page_path = first_page_path.replace('"', '').replace("'", "")
        last_page_path = last_page_path.replace('"', '').replace("'", "")

       
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
           
            print(f"{i}. دانشجو: {request['student_id']} - عنوان: {request.get('thesis_title', 'بدون عنوان')}")
        
        try:
            choice = int(input("\nشماره درخواست برای بررسی را انتخاب کنید: ")) - 1
            if 0 <= choice < len(requests):
                request = requests[choice]
                
                print(f"\nبررسی درخواست دفاع دانشجو {request['student_id']}")
                print(f"عنوان: {request.get('thesis_title', 'بدون عنوان')}")
                print(f"چکیده: {request.get('abstract', '')[:100]}...")
                
                action = input("آیا می‌خواهید این درخواست را تأیید کنید؟ (y/n): ").lower()
                
                if action == 'y':
                    defense_date = input("تاریخ دفاع (YYYY-MM-DD): ")
                    internal_evaluator = input("کد داور داخلی: ")
                    external_evaluator = input("کد داور خارجی: ")
                    
                    
                    success, message = self.professor_service.process_defense_request(
                        request['student_id'], self.current_user.user_id, True, defense_date, internal_evaluator, external_evaluator
                    )
                    print(message)
                elif action == 'n':
                    reason = input("دلیل رد درخواست: ")
                    
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
                
               
                guidance_score = float(input("نمره استاد راهنما: "))
                attendees = input("حاضرین جلسه (با کاما جدا کنید): ").split(',')
                defense_result = input("نتیجه دفاع (defended/redefense): ")
                
               
                success, message = self.professor_service.complete_defense_process(
                    defense['student_id'], 
                    guidance_score, 
                    None,  
                    None,  
                    [a.strip() for a in attendees], 
                    defense_result
                )
                print(message)
            else:
                print("شماره جلسه دفاع نامعتبر!")
        except ValueError:
            print("لطفاً مقادیر عددی را صحیح وارد کنید!")
    def grade_as_internal_evaluator(self, evaluator_service):
        """ثبت نمره به عنوان داور داخلی"""
        print("\n--- ثبت نمره به عنوان داور داخلی ---")
        
        
        internal_evaluator_theses = evaluator_service.get_internal_theses_to_evaluate(self.current_user.user_id)
        
        if not internal_evaluator_theses:
            print("هیچ پایان‌نامه‌ای به عنوان داور داخلی ندارید.")
            return
        
        print("پایان‌نامه‌هایی که داور داخلی آنها هستید:")
        for i, thesis in enumerate(internal_evaluator_theses, 1):
            
            student_id = thesis.get('student_id')
            student = self.auth_service.get_user(student_id)
            student_name = student.name if student else "نامشخص"
            
            current_grade = thesis.get('internal_score', 'ثبت نشده')
            print(f"{i}. {thesis['title']} - دانشجو: {student_name} - نمره فعلی: {current_grade}")
        
        try:
            thesis_choice = int(input("شماره پایان‌نامه مورد نظر را انتخاب کنید: ")) - 1
            if thesis_choice < 0 or thesis_choice >= len(internal_evaluator_theses):
                print("شماره نامعتبر!")
                return
            
            selected_thesis = internal_evaluator_theses[thesis_choice]
            student_id = selected_thesis.get('student_id')
            
            
            grade = float(input("نمره پایان‌نامه (0-20): "))
            if grade < 0 or grade > 20:
                print("نمره باید بین 0 تا 20 باشد!")
                return
            
            
            success, message = evaluator_service.submit_internal_evaluation(
                student_id, self.current_user.user_id, grade
            )
            print(message)
                
        except ValueError:
            print("لطفاً عدد وارد کنید!")
        except Exception as e:
            print(f"خطا: {e}")

    def search_theses(self):
        
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
        print("=" * 80)
        
        for i, thesis in enumerate(results, 1):
            print(f"\n{i}. **عنوان:** {thesis.get('title', 'نامشخص')}")
            print(f"   **نویسنده:** {thesis.get('student_id', 'نامشخص')}")
            print(f"   **استاد راهنما:** {thesis.get('professor_id', 'نامشخص')}")
            print(f"   **سال/نیمسال:** {thesis.get('year', 'نامشخص')} - {thesis.get('semester', 'نامشخص')}")
            
            
            abstract = thesis.get('abstract', '')
            if abstract and len(abstract) > 150:
                abstract = abstract[:150] + "..."
            print(f"   **چکیده:** {abstract}")
            
            
            keywords = thesis.get('keywords', [])
            if keywords:
                print(f"   **کلمات کلیدی:** {', '.join(keywords)}")
            
            
            internal_eval = thesis.get('internal_evaluator', 'نامشخص')
            external_eval = thesis.get('external_evaluator', 'نامشخص')
            print(f"   **داوران:** داخلی: {internal_eval}, خارجی: {external_eval}")
            
            
            final_score = thesis.get('final_score')
            grade = self.search_service.get_grade(final_score)
            print(f"   **نمره نهایی:** {final_score or 'ثبت نشده'} ({grade})")
            
           
            pdf_path = thesis.get('pdf_path')
            if pdf_path:
                print(f"   **لینک دانلود:** {pdf_path}")
            else:
                print(f"   **لینک دانلود:** فایل موجود نیست")
            
            print("-" * 80)
        
       
        try:
            choice = input("\nبرای مشاهده جزئیات کامل یک پایان‌نامه شماره آن را وارد کنید (یا Enter برای بازگشت): ")
            if choice.strip():
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(results):
                    thesis = results[choice_idx]
                    self.show_thesis_details(thesis)
        except ValueError:
            print("ورودی نامعتبر!")

    def show_thesis_details(self, thesis):
        
        print("\n" + "=" * 80)
        print("جزئیات کامل پایان‌نامه")
        print("=" * 80)
        
        print(f"**عنوان:** {thesis.get('title', 'نامشخص')}")
        print(f"**نویسنده:** {thesis.get('student_id', 'نامشخص')}")
        print(f"**استاد راهنما:** {thesis.get('professor_id', 'نامشخص')}")
        print(f"**سال/نیمسال:** {thesis.get('year', 'نامشخص')} - {thesis.get('semester', 'نامشخص')}")
        print(f"**تاریخ دفاع:** {thesis.get('defense_date', 'نامشخص')}")
        
        
        internal_eval = thesis.get('internal_evaluator', 'نامشخص')
        external_eval = thesis.get('external_evaluator', 'نامشخص')
        print(f"**داور داخلی:** {internal_eval}")
        print(f"**داور خارجی:** {external_eval}")
        
       
        print(f"**چکیده:** {thesis.get('abstract', 'ثبت نشده')}")
        
        
        keywords = thesis.get('keywords', [])
        print(f"**کلمات کلیدی:** {', '.join(keywords) if keywords else 'ثبت نشده'}")
        
        
        guidance_score = thesis.get('guidance_score')
        internal_score = thesis.get('internal_score')
        external_score = thesis.get('external_score')
        final_score = thesis.get('final_score')
        grade = self.search_service.get_grade(final_score)
        
        print(f"**نمره استاد راهنما:** {guidance_score or 'ثبت نشده'}")
        print(f"**نمره داور داخلی:** {internal_score or 'ثبت نشده'}")
        print(f"**نمره داور خارجی:** {external_score or 'ثبت نشده'}")
        print(f"**نمره نهایی:** {final_score or 'ثبت نشده'} ({grade})")
        
        
        attendees = thesis.get('attendees', [])
        print(f"**حاضرین جلسه:** {', '.join(attendees) if attendees else 'ثبت نشده'}")
        
       
        pdf_path = thesis.get('pdf_path')
        first_page = thesis.get('first_page_path')
        last_page = thesis.get('last_page_path')
        
        print(f"**فایل PDF:** {pdf_path or 'موجود نیست'}")
        print(f"**تصویر صفحه اول:** {first_page or 'موجود نیست'}")
        print(f"**تصویر صفحه آخر:** {last_page or 'موجود نیست'}")
        
        print("=" * 80)
    def show_evaluator_menu(self):
       
        from services.evaluator_service import EvaluatorService
        
        evaluator_service = EvaluatorService()
        
        while True:
            print("\n" + "="*50)
            print("منوی داور")
            print("="*50)
            print("1. ثبت نمره پایان‌نامه‌ها")
            print("2. جستجو در بانک پایان‌نامه‌ها")
            print("3. تغییر رمز عبور")
            print("4. خروج از حساب کاربری")  
            
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
                break  
            else:
                print("گزینه نامعتبر!")
    def evaluate_theses(self, evaluator_service):
        
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
    
    def email_menu(self):
       
        from services.email_service import EmailService
        
        email_service = EmailService()
        
      
        user_email = None
        for user in email_service.users:
            if user['user_id'] == self.current_user.user_id:
                user_email = user['email']
                break
        
        if not user_email:
            print("ایمیل کاربر یافت نشد!")
            return
        
        while True:
            stats = email_service.get_email_stats(user_email)
            print(f"\n📧 سیستم ایمیل ({user_email})")
            print("="*50)
            print(f"📭 خوانده نشده: {stats['unread']} | 📬 خوانده شده: {stats['read']} | 📁 آرشیو: {stats['archived']}")
            print("="*50)
            print("1. inbox (صندوق ورودی)")
            print("2. ایمیل‌های ارسال شده")
            print("3. ایمیل‌های آرشیو شده")
            print("4. ارسال ایمیل جدید")
            print("5. جستجو در ایمیل‌ها")
            print("6. بازگشت به منوی اصلی")
            
            choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
            
            if choice == "1":
                self.view_inbox(email_service, user_email)
            elif choice == "2":
                self.view_sent_emails(email_service, user_email)
            elif choice == "3":
                self.view_archived_emails(email_service, user_email)
            elif choice == "4":
                self.send_new_email(email_service, user_email)
            elif choice == "5":
                self.search_emails(email_service, user_email)
            elif choice == "6":
                break
            else:
                print("گزینه نامعتبر!")  
    def send_new_email(self, email_service, user_email):
        
        print("\n📤 ارسال ایمیل جدید")
        print("="*30)
        
        receiver_email = input("ایمیل گیرنده: ")
        subject = input("موضوع ایمیل: ")
        print("متن ایمیل (پس از نوشتن، Enter بزنید):")
        content = input()
        
        success, message = email_service.send_email(
            user_email, receiver_email, subject, content
        )
        print(message)

    def view_inbox(self, email_service, user_email):
        
        emails = email_service.get_inbox(user_email)
        
        if not emails:
            print("📭 صندوق ورودی شما خالی است.")
            return
        
        print(f"\n📧 صندوق ورودی ({len(emails)} ایمیل)")
        print("="*50)
        
        for i, email in enumerate(emails, 1):
            status = "📭" if not email.is_read else "📬"
            print(f"{i}. {status} از: {email.sender_email} - موضوع: {email.subject}")
        
        try:
            email_choice = int(input("\nشماره ایمیل برای مشاهده (یا 0 برای بازگشت): "))
            if email_choice == 0:
                return
            if 1 <= email_choice <= len(emails):
                email = emails[email_choice-1]
                self.show_email_detail(email, email_service, user_email)
            else:
                print("شماره ایمیل نامعتبر!")
        except ValueError:
            print("لطفاً عدد وارد کنید!")

    def show_email_detail(self, email, email_service, user_email):
        
        print(f"\n📧 موضوع: {email.subject}")
        print(f"👤 از: {email.sender_email}")
        print(f"⏰ تاریخ: {email.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print("="*40)
        print(f"📝 متن ایمیل:\n{email.content}")
        print("="*40)
        
        if not email.is_read:
            email_service.mark_as_read(email.email_id, user_email)
            print("✅ ایمیل به عنوان خوانده شده علامت گذاری شد")
        
       
        print("\n📋 گزینه‌های مدیریت:")
        print("1. آرشیو کردن ایمیل")
        print("2. بازگشت")
        
        choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
        
        if choice == "1":
            success, message = email_service.archive_email(email.email_id, user_email)
            print(message)

    def view_sent_emails(self, email_service, user_email):
       
        emails = email_service.get_sent_emails(user_email)
        
        if not emails:
            print("📤 هیچ ایمیل ارسال شده‌ای ندارید.")
            return
        
        print(f"\n📤 ایمیل‌های ارسال شده ({len(emails)} ایمیل)")
        print("="*50)
        
        for i, email in enumerate(emails, 1):
            print(f"{i}. به: {email.receiver_email} - موضوع: {email.subject}")
        
        try:
            email_choice = int(input("\nشماره ایمیل برای مشاهده (یا 0 برای بازگشت): "))
            if email_choice == 0:
                return
            if 1 <= email_choice <= len(emails):
                email = emails[email_choice-1]
                self.show_sent_email_detail(email)
            else:
                print("شماره ایمیل نامعتبر!")
        except ValueError:
            print("لطفاً عدد وارد کنید!")

    def show_sent_email_detail(self, email):
       
        print(f"\n📧 موضوع: {email.subject}")
        print(f"👤 به: {email.receiver_email}")
        print(f"⏰ تاریخ: {email.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print("="*40)
        print(f"📝 متن ایمیل:\n{email.content}")
        print("="*40)
        
        input("\n↵ برای ادامه Enter بزنید")

    def view_archived_emails(self, email_service, user_email):
        
        emails = email_service.get_archived_emails(user_email)
        
        if not emails:
            print("📁 هیچ ایمیل آرشیو شده‌ای ندارید.")
            return
        
        print(f"\n📁 ایمیل‌های آرشیو شده ({len(emails)} ایمیل)")
        print("="*50)
        
        for i, email in enumerate(emails, 1):
            status = "📭" if not email.is_read else "📬"
            print(f"{i}. {status} از: {email.sender_email} - موضوع: {email.subject}")
        
        try:
            email_choice = int(input("\nشماره ایمیل برای مشاهده (یا 0 برای بازگشت): "))
            if email_choice == 0:
                return
            if 1 <= email_choice <= len(emails):
                email = emails[email_choice-1]
                self.show_email_detail(email, email_service, user_email)
            else:
                print("شماره ایمیل نامعتبر!")
        except ValueError:
            print("لطفاً عدد وارد کنید!")

    def search_emails(self, email_service, user_email):
        
        print("\n🔍 جستجو در ایمیل‌ها")
        print("="*30)
        
        query = input("عبارت جستجو: ")
        
        if not query.strip():
            print("لطفاً عبارتی برای جستجو وارد کنید.")
            return
        
        results = email_service.search_emails(user_email, query)
        
        if not results:
            print("❌ هیچ نتیجه‌ای یافت نشد.")
            return
        
        print(f"\n✅ {len(results)} نتیجه یافت شد:")
        print("="*40)
        
        for i, email in enumerate(results, 1):
            status = "📭" if not email.is_read else "📬"
            print(f"{i}. {status} از: {email.sender_email} - موضوع: {email.subject}")
        
        try:
            email_choice = int(input("\nشماره ایمیل برای مشاهده (یا 0 برای بازگشت): "))
            if email_choice == 0:
                return
            if 1 <= email_choice <= len(results):
                email = results[email_choice-1]
                self.show_email_detail(email, email_service, user_email)
            else:
                print("شماره ایمیل نامعتبر!")
        except ValueError:
            print("لطفاً عدد وارد کنید!")         
def main():
    system = ThesisManagementSystem()
    system.run()

if __name__ == "__main__":
    main()

#https://github.com/hastigrfg/thesis_management_system
