import json
from datetime import datetime
from utils.date_utils import get_current_date, format_date

class Email:
    def __init__(self, email_id, sender_email, receiver_email, subject, content, 
                 timestamp=None, is_read=False, is_archived=False, labels=None):
        self.email_id = email_id
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject
        self.content = content
        self.timestamp = timestamp or get_current_date()
        self.is_read = is_read
        self.is_archived = is_archived
        self.labels = labels or []
        self.attachments = []
    
    def mark_as_read(self):
        self.is_read = True
    
    def mark_as_unread(self):
        self.is_read = False
    
    def archive(self):
        self.is_archived = True
    
    def unarchive(self):
        self.is_archived = False
    
    def add_label(self, label):
        if label not in self.labels:
            self.labels.append(label)
    
    def remove_label(self, label):
        if label in self.labels:
            self.labels.remove(label)
    
    def add_attachment(self, file_name, file_path):
        self.attachments.append({"name": file_name, "path": file_path})
    
    def to_dict(self):
        return {
            "email_id": self.email_id,
            "sender_email": self.sender_email,
            "receiver_email": self.receiver_email,
            "subject": self.subject,
            "content": self.content,
            "timestamp": format_date(self.timestamp),
            "is_read": self.is_read,
            "is_archived": self.is_archived,
            "labels": self.labels,
            "attachments": self.attachments
        }
    
    @classmethod
    def from_dict(cls, data):
        from utils.date_utils import parse_date
        
        email = cls(
            data["email_id"],
            data["sender_email"],
            data["receiver_email"],
            data["subject"],
            data["content"]
        )
        
        email.timestamp = parse_date(data["timestamp"]) if data["timestamp"] else None
        email.is_read = data.get("is_read", False)
        email.is_archived = data.get("is_archived", False)
        email.labels = data.get("labels", [])
        email.attachments = data.get("attachments", [])
        
        return email
    
    def __str__(self):
        status = "📭" if not self.is_read else "📬"
        return f"{status} از: {self.sender_email} - موضوع: {self.subject}"
