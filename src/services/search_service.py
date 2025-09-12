import json
from config import THESES_FILE

class SearchService:
    def __init__(self, theses_file=THESES_FILE):
        self.theses_file = theses_file
        self.theses = self.load_theses()
    
    def load_theses(self):
        try:
            with open(self.theses_file, 'r', encoding='utf-8') as file:
                theses_data = json.load(file)
                return [t for t in theses_data if t.get("defense_result") == "defended"]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def search_theses(self, query=None, professor=None, keyword=None, author=None, year=None, evaluator=None):
        results = self.theses.copy()
        
        if query:
            results = [t for t in results 
                      if query.lower() in t.get("title", "").lower() 
                      or query.lower() in t.get("abstract", "").lower()]
        
        if professor:
            results = [t for t in results if str(professor) in str(t.get("professor_id", ""))]
        
        if keyword:
            results = [t for t in results 
                      if any(keyword.lower() in k.lower() for k in t.get("keywords", []))]
        
        if author:
            results = [t for t in results if str(author) in str(t.get("student_id", ""))]
        
        if year:
            results = [t for t in results if t.get("year") == year]
        
        if evaluator:
            results = [t for t in results 
                      if (str(evaluator) in str(t.get("internal_evaluator", "")) or 
                          str(evaluator) in str(t.get("external_evaluator", "")))]
        
        return results
    
    def get_thesis_details(self, thesis_id):
        thesis = next((t for t in self.theses if t["student_id"] == thesis_id), None)
        if thesis and thesis.get("defense_result") == "defended":
            return thesis
        return None
    
    def get_grade(self, final_score):
        if final_score is None:
            return "ثبت نشده"
        if final_score >= 17:
            return "الف"
        elif final_score >= 14:
            return "ب"
        elif final_score >= 12:
            return "ج"
        else:
            return "د"
