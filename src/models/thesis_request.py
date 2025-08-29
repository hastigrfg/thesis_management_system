from utils.date_utils import get_current_date, format_date

class ThesisRequest:
    def __init__(self, student_id, course_id, professor_id, request_date=None, 
                 status="pending", approval_date=None, rejection_reason=None):
        self.student_id = student_id
        self.course_id = course_id
        self.professor_id = professor_id
        self.request_date = request_date or get_current_date()
        self.status = status  # pending, approved, rejected
        self.approval_date = approval_date
        self.rejection_reason = rejection_reason
    
    def approve(self):
        self.status = "approved"
        self.approval_date = get_current_date()
        self.rejection_reason = None
    
    def reject(self, reason):
        self.status = "rejected"
        self.approval_date = None
        self.rejection_reason = reason
    
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "course_id": self.course_id,
            "professor_id": self.professor_id,
            "request_date": format_date(self.request_date),
            "status": self.status,
            "approval_date": format_date(self.approval_date) if self.approval_date else None,
            "rejection_reason": self.rejection_reason
        }
    
    @classmethod
    def from_dict(cls, data):
        from utils.date_utils import parse_date
        
        request = cls(
            student_id=data["student_id"],
            course_id=data["course_id"],
            professor_id=data["professor_id"],
            status=data["status"],
            rejection_reason=data.get("rejection_reason")
        )
        
        request.request_date = parse_date(data["request_date"]) if data["request_date"] else None
        request.approval_date = parse_date(data["approval_date"]) if data.get("approval_date") else None
        
        return request
