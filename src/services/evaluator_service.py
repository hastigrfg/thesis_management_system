import json
from config import THESES_FILE
from utils.date_utils import get_current_date

class EvaluatorService:
    def __init__(self, theses_file=THESES_FILE):
        self.theses_file = theses_file
    
    def get_theses_to_evaluate(self, professor_id):
        
        theses_to_evaluate = []
        
        try:
            
            with open(self.theses_file, 'r', encoding='utf-8') as file:
                theses = json.load(file)
            
            for thesis in theses:
                is_external_evaluator = thesis.get("external_evaluator") == professor_id
                external_score_not_set = thesis.get("external_score") is None
                
                if is_external_evaluator and external_score_not_set:
                    theses_to_evaluate.append(thesis)
        
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        
        if not theses_to_evaluate:
            try:
                with open("data/theses.jsons", 'r', encoding='utf-8') as file:
                    theses.json = json.load(file)
                
                for request in theses.json:
                    if (request.get("external_evaluator") == professor_id and 
                        request.get("status") == "scheduled"):
                       
                        thesis_data = {
                            "student_id": request["student_id"],
                            "professor_id": request["professor_id"],
                            "title": request.get("thesis_title", ""),
                            "abstract": request.get("abstract", ""),
                            "keywords": request.get("keywords", []),
                            "external_evaluator": request.get("external_evaluator"),
                            "external_score": None
                        }
                        theses_to_evaluate.append(thesis_data)
                        
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        
        return theses_to_evaluate

    def submit_evaluation(self, student_id, professor_id, score):
        
        try:
            with open(self.theses_file, 'r', encoding='utf-8') as file:
                theses = json.load(file)
            
            thesis_index = -1
            for i, thesis in enumerate(theses):
                if thesis["student_id"] == student_id:
                    thesis_index = i
                    break
            
            if thesis_index == -1:
                return False, "پایان‌نامه یافت نشد"
            
            thesis = theses[thesis_index]
            evaluator_type = None
            
          
            if thesis.get("internal_evaluator") == professor_id:
                if thesis.get("internal_score") is not None:
                    return False, "شما قبلاً نمره این پایان‌نامه را ثبت کرده‌اید"
                theses[thesis_index]["internal_score"] = score
                evaluator_type = "داخلی"
            elif thesis.get("external_evaluator") == professor_id:
                if thesis.get("external_score") is not None:
                    return False, "شما قبلاً نمره این پایان‌نامه را ثبت کرده‌اید"
                theses[thesis_index]["external_score"] = score
                evaluator_type = "خارجی"
            else:
                return False, "شما داور این پایان‌نامه نیستید"
            
            
            print(f"شما به عنوان داور {evaluator_type} این پایان‌نامه هستید")
            
           
            self._calculate_final_score_if_ready(theses[thesis_index])
            
            with open(self.theses_file, 'w', encoding='utf-8') as file:
                json.dump(theses, file, ensure_ascii=False, indent=4)
            
            return True, f"نمره داور {evaluator_type} با موفقیت ثبت شد"
            
        except Exception as e:
            return False, f"خطا در ثبت نمره: {str(e)}"
        
    
    def _calculate_final_score_if_ready(self, thesis):
        
        if (thesis.get("guidance_score") is not None and
            thesis.get("internal_score") is not None and
            thesis.get("external_score") is not None):
            
            guidance = thesis.get("guidance_score", 0)
            internal = thesis.get("internal_score", 0)
            external = thesis.get("external_score", 0)
            
            thesis["final_score"] = round((guidance + internal + external) / 3, 2)
            
           
            if thesis["final_score"] >= 12:
                thesis["defense_result"] = "defended"
            else:
                thesis["defense_result"] = "redefense"
            
            thesis["completion_date"] = get_current_date().strftime("%Y-%m-%d %H:%M:%S")

    def evaluate_as_internal_evaluator(self, evaluator_service):
        
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
    def get_internal_theses_to_evaluate(self, professor_id):
       
        try:
            with open(self.theses_file, 'r', encoding='utf-8') as file:
                theses = json.load(file)
            
            theses_to_evaluate = []
            for thesis in theses:
                is_internal_evaluator = thesis.get("internal_evaluator") == professor_id
                internal_score_not_set = thesis.get("internal_score") is None
                
                if is_internal_evaluator and internal_score_not_set:
                    theses_to_evaluate.append(thesis)
            
            return theses_to_evaluate
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def submit_internal_evaluation(self, student_id, professor_id, score):
       
        try:
            with open(self.theses_file, 'r', encoding='utf-8') as file:
                theses = json.load(file)
            
            thesis_index = -1
            for i, thesis in enumerate(theses):
                if thesis["student_id"] == student_id:
                    thesis_index = i
                    break
            
            if thesis_index == -1:
                return False, "پایان‌نامه یافت نشد"
            
            
            if theses[thesis_index].get("internal_evaluator") != professor_id:
                return False, "شما داور داخلی این پایان‌نامه نیستید"
            
           
            if theses[thesis_index].get("internal_score") is not None:
                return False, "شما قبلاً نمره این پایان‌نامه را ثبت کرده‌اید"
            
           
            theses[thesis_index]["internal_score"] = score
            
           
            self._calculate_final_score_if_ready(theses[thesis_index])
            
            with open(self.theses_file, 'w', encoding='utf-8') as file:
                json.dump(theses, file, ensure_ascii=False, indent=4)
            
            return True, "نمره داور داخلی با موفقیت ثبت شد"
            
        except Exception as e:
            return False, f"خطا در ثبت نمره: {str(e)}"
