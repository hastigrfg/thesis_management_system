from utils.date_utils import get_current_date, format_date

class Thesis:
    def __init__(self, student_id, professor_id, title, abstract, keywords,
                 pdf_path, first_page_path, last_page_path, year, semester,
                 defense_date, internal_evaluator, external_evaluator,
                 attendees=None, guidance_score=None, internal_score=None,
                 external_score=None, final_score=None, defense_result=None,
                 completion_date=None):
        self.student_id = student_id
        self.professor_id = professor_id
        self.title = title
        self.abstract = abstract
        self.keywords = keywords or []
        self.pdf_path = pdf_path
        self.first_page_path = first_page_path
        self.last_page_path = last_page_path
        self.year = year
        self.semester = semester
        self.defense_date = defense_date
        self.internal_evaluator = internal_evaluator
        self.external_evaluator = external_evaluator
        self.attendees = attendees or []
        self.guidance_score = guidance_score
        self.internal_score = internal_score
        self.external_score = external_score
        self.final_score = final_score
        self.defense_result = defense_result  # defended, redefense
        self.completion_date = completion_date or get_current_date()
    
    def calculate_final_score(self):
        if self.guidance_score and self.internal_score and self.external_score:
            self.final_score = (self.guidance_score + self.internal_score + self.external_score) / 3
            return self.final_score
        return None
    
    def get_grade(self):
        if not self.final_score:
            return None
        
        if self.final_score >= 17:
            return "الف"
        elif self.final_score >= 14:
            return "ب"
        elif self.final_score >= 12:
            return "ج"
        else:
            return "د"
    
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "professor_id": self.professor_id,
            "title": self.title,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "pdf_path": self.pdf_path,
            "first_page_path": self.first_page_path,
            "last_page_path": self.last_page_path,
            "year": self.year,
            "semester": self.semester,
            "defense_date": format_date(self.defense_date) if self.defense_date else None,
            "internal_evaluator": self.internal_evaluator,
            "external_evaluator": self.external_evaluator,
            "attendees": self.attendees,
            "guidance_score": self.guidance_score,
            "internal_score": self.internal_score,
            "external_score": self.external_score,
            "final_score": self.final_score,
            "defense_result": self.defense_result,
            "completion_date": format_date(self.completion_date)
        }
    
    @classmethod
    def from_dict(cls, data):
        from utils.date_utils import parse_date
        
        thesis = cls(
            student_id=data["student_id"],
            professor_id=data["professor_id"],
            title=data["title"],
            abstract=data["abstract"],
            keywords=data.get("keywords", []),
            pdf_path=data["pdf_path"],
            first_page_path=data["first_page_path"],
            last_page_path=data["last_page_path"],
            year=data["year"],
            semester=data["semester"],
            internal_evaluator=data["internal_evaluator"],
            external_evaluator=data["external_evaluator"],
            attendees=data.get("attendees", []),
            guidance_score=data.get("guidance_score"),
            internal_score=data.get("internal_score"),
            external_score=data.get("external_score"),
            final_score=data.get("final_score"),
            defense_result=data.get("defense_result")
        )
        
        thesis.defense_date = parse_date(data["defense_date"]) if data.get("defense_date") else None
        thesis.completion_date = parse_date(data["completion_date"]) if data.get("completion_date") else None
        
        return thesis
