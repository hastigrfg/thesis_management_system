import json
from datetime import datetime
from utils.date_utils import get_current_date, format_date

class MeetingMinutes:
    def __init__(self, minutes_id, thesis_id, meeting_date, attendees, 
                 agenda, decisions, actions, created_by):
        self.minutes_id = minutes_id
        self.thesis_id = thesis_id
        self.meeting_date = meeting_date
        self.attendees = attendees
        self.agenda = agenda
        self.decisions = decisions
        self.actions = actions
        self.created_by = created_by
        self.created_at = get_current_date()
    
    def generate_template(self):
        return f"""
        صورت جلسه دفاع پایان‌نامه
        ===========================
        
        شناسه پایان‌نامه: {self.thesis_id}
        تاریخ جلسه: {self.meeting_date}
        
        حاضرین جلسه:
        {', '.join(self.attendees)}
        
        دستور جلسه:
        {self.agenda}
        
        تصمیمات اتخاذ شده:
        {self.decisions}
        
        اقدامات بعدی:
        {self.actions}
        
        ثبت شده توسط: {self.created_by}
        تاریخ ثبت: {format_date(self.created_at)}
        """
    
    def to_dict(self):
        return {
            "minutes_id": self.minutes_id,
            "thesis_id": self.thesis_id,
            "meeting_date": self.meeting_date,
            "attendees": self.attendees,
            "agenda": self.agenda,
            "decisions": self.decisions,
            "actions": self.actions,
            "created_by": self.created_by,
            "created_at": format_date(self.created_at)
        }
    
    @classmethod
    def from_dict(cls, data):
        minutes = cls(
            data["minutes_id"],
            data["thesis_id"],
            data["meeting_date"],
            data["attendees"],
            data["agenda"],
            data["decisions"],
            data["actions"],
            data["created_by"]
        )
        minutes.created_at = datetime.strptime(data["created_at"], '%Y-%m-%d %H:%M:%S')
        return minutes
