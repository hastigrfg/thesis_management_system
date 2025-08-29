from utils.date_utils import get_current_date, format_date

class DefenseRequest:
    def __init__(self, student_id, professor_id, request_date=None, 
                 thesis_title=None, abstract=None, keywords=None,
                 pdf_path=None, first_page_path=None, last_page_path=None,
                 status="pending", defense_date=None, internal_evaluator=None,
                 external_evaluator=None, rejection_reason=None):
        self.student_id = student_id
        self.professor_id = professor_id
        self.request_date = request_date or get_current_date()
        self.thesis_title = thesis_title
        self.abstract = abstract
        self.keywords = keywords or []
        self.pdf_path = pdf_path
        self.first_page_path = first_page_path
        self.last_page_path = last_page_path
        self.status = status  # pending, approved, rejected, scheduled, completed
        self.defense_date = defense_date
        self.internal_evaluator = internal_evaluator
        self.external_evaluator = external_evaluator
        self.rejection_reason = rejection_reason
    
    def approve(self, defense_date, internal_evaluator, external_evaluator):
        self.status = "scheduled"
        self.defense_date = defense_date
        self.internal_evaluator = internal_evaluator
        self.external_evaluator = external_evaluator
        self.rejection_reason = None
    
    def reject(self, reason):
        self.status = "rejected"
        self.defense_date = None
        self.internal_evaluator = None
        self.external_evaluator = None
        self.rejection_reason = reason
    
    def complete(self):
        self.status = "completed"
    
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "professor_id": self.professor_id,
            "request_date": format_date(self.request_date),
            "thesis_title": self.thesis_title,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "pdf_path": self.pdf_path,
            "first_page_path": self.first_page_path,
            "last_page_path": self.last_page_path,
            "status": self.status,
            "defense_date": format_date(self.defense_date) if self.defense_date else None,
            "internal_evaluator": self.internal_evaluator,
            "external_evaluator": self.external_evaluator,
            "rejection_reason": self.rejection_reason
        }
    
    @classmethod
    def from_dict(cls, data):
        from utils.date_utils import parse_date
        
        request = cls(
            student_id=data["student_id"],
            professor_id=data["professor_id"],
            thesis_title=data.get("thesis_title"),
            abstract=data.get("abstract"),
            keywords=data.get("keywords", []),
            pdf_path=data.get("pdf_path"),
            first_page_path=data.get("first_page_path"),
            last_page_path=data.get("last_page_path"),
            status=data.get("status", "pending"),
            internal_evaluator=data.get("internal_evaluator"),
            external_evaluator=data.get("external_evaluator"),
            rejection_reason=data.get("rejection_reason")
        )
        
        request.request_date = parse_date(data["request_date"]) if data["request_date"] else None
        request.defense_date = parse_date(data["defense_date"]) if data.get("defense_date") else None
        
        return request
