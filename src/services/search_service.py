import json
from config import THESES_FILE

class SearchService:
    def __init__(self, theses_file=THESES_FILE):
        self.theses_file = theses_file
        self.theses = self.load_theses()
    
    def load_theses(self):
        try:
            with open(self.theses_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def search_theses(self, query=None, professor=None, keyword=None, author=None, year=None, evaluator=None):
        results = self.theses.copy()
        
        if query:
            results = [t for t in results 
                      if query.lower() in t.get("title", "").lower() 
                      or query.lower() in t.get("abstract", "").lower()]
        
        if professor:
            results = [t for t in results if professor.lower() in t.get("professor_id", "").lower()]
        
        if keyword:
            results = [t for t in results 
                      if any(keyword.lower() in k.lower() for k in t.get("keywords", []))]
        
        if author:
            results = [t for t in results if author.lower() in t.get("student_id", "").lower()]
        
        if year:
            results = [t for t in results if t.get("year") == year]
        
        if evaluator:
            results = [t for t in results 
                      if evaluator.lower() in t.get("internal_evaluator", "").lower()
                      or evaluator.lower() in t.get("external_evaluator", "").lower()]
        
        return results
    
    def get_thesis_details(self, thesis_id):
        return next((t for t in self.theses if t["student_id"] == thesis_id), None)
