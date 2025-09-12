import json
from ..models.meeting_minutes import MeetingMinutes
from config import MINUTES_FILE
from datetime import datetime

class MinutesService:
    def __init__(self, minutes_file=MINUTES_FILE):
        self.minutes_file = minutes_file
        self.minutes_list = self.load_minutes()
    
    def load_minutes(self):
        try:
            with open(self.minutes_file, 'r', encoding='utf-8') as file:
                minutes_data = json.load(file)
                return [MeetingMinutes.from_dict(data) for data in minutes_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_minutes(self):
        minutes_data = [minutes.to_dict() for minutes in self.minutes_list]
        with open(self.minutes_file, 'w', encoding='utf-8') as file:
            json.dump(minutes_data, file, ensure_ascii=False, indent=4)
    
    def create_minutes(self, thesis_id, meeting_date, attendees, agenda, decisions, actions, created_by):
        minutes_id = f"min_{len(self.minutes_list) + 1}_{int(datetime.now().timestamp())}"
        
        new_minutes = MeetingMinutes(
            minutes_id, thesis_id, meeting_date, attendees, 
            agenda, decisions, actions, created_by
        )
        
        self.minutes_list.append(new_minutes)
        self.save_minutes()
        
        return True, "صورت جلسه با موفقیت ثبت شد", new_minutes.generate_template()
    
    def get_thesis_minutes(self, thesis_id):
        return [m for m in self.minutes_list if m.thesis_id == thesis_id]
    
    def get_all_minutes(self):
        return self.minutes_list
