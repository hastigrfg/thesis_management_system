import json
from datetime import datetime
from config import THESIS_REQUESTS_FILE, DEFENSE_REQUESTS_FILE, MESSAGES_FILE

class DashboardService:
    def __init__(self):
        self.thesis_requests_file = THESIS_REQUESTS_FILE
        self.defense_requests_file = DEFENSE_REQUESTS_FILE
        self.messages_file = MESSAGES_FILE
    
    def get_student_dashboard(self, student_id):
        try:
            
            with open(self.thesis_requests_file, 'r', encoding='utf-8') as f:
                thesis_requests = json.load(f)
            
            with open(self.defense_requests_file, 'r', encoding='utf-8') as f:
                defense_requests = json.load(f)
            
            with open(self.messages_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            
            
            student_thesis_requests = [r for r in thesis_requests if r['student_id'] == student_id]
            student_defense_requests = [r for r in defense_requests if r['student_id'] == student_id]
            student_messages = [m for m in messages if m['receiver_id'] == student_id]
            
            
            stats = {
                'total_thesis_requests': len(student_thesis_requests),
                'approved_theses': len([r for r in student_thesis_requests if r['status'] == 'approved']),
                'pending_requests': len([r for r in student_thesis_requests if r['status'] == 'pending']),
                'defense_requests': len(student_defense_requests),
                'unread_messages': len([m for m in student_messages if not m['is_read']]),
                'latest_activity': self._get_latest_activity(student_thesis_requests, student_defense_requests)
            }
            
            return {
                'success': True,
                'stats': stats,
                'recent_requests': student_thesis_requests[-5:],  
                'recent_messages': student_messages[-3:]  
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _get_latest_activity(self, thesis_requests, defense_requests):
        activities = []
        
        for req in thesis_requests:
            activities.append({
                'type': 'thesis_request',
                'date': req['request_date'],
                'status': req['status'],
                'title': 'درخواست پایان‌نامه'
            })
        
        for req in defense_requests:
            activities.append({
                'type': 'defense_request',
                'date': req['request_date'],
                'status': req['status'],
                'title': 'درخواست دفاع'
            })
        
       
        activities.sort(key=lambda x: x['date'], reverse=True)
        return activities[:10] 
    
   
    
    def get_professor_dashboard(self, professor_id):
        try:
            
            with open(self.thesis_requests_file, 'r', encoding='utf-8') as f:
                thesis_requests = json.load(f)
            
            with open(self.defense_requests_file, 'r', encoding='utf-8') as f:
                defense_requests = json.load(f)
            
            with open(self.messages_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            
            
            professor_thesis_requests = [r for r in thesis_requests if r['professor_id'] == professor_id]
            professor_defense_requests = [r for r in defense_requests if r['professor_id'] == professor_id]
            professor_messages = [m for m in messages if m['receiver_id'] == professor_id]
            
            # محاسبه آمار
            stats = {
                'total_students': len(set(r['student_id'] for r in professor_thesis_requests)),
                'pending_approvals': len([r for r in professor_thesis_requests if r['status'] == 'pending']),
                'scheduled_defenses': len([r for r in professor_defense_requests if r['status'] == 'scheduled']),
                'completed_defenses': len([r for r in professor_defense_requests if r['status'] == 'completed']),
                'unread_messages': len([m for m in professor_messages if not m['is_read']]),
                'guidance_capacity': self._get_guidance_capacity(professor_id)
            }
            
            return {
                'success': True,
                'stats': stats,
                'pending_requests': [r for r in professor_thesis_requests if r['status'] == 'pending'],
                'upcoming_defenses': [r for r in professor_defense_requests if r['status'] == 'scheduled'],
                'recent_messages': professor_messages[-3:]
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _get_guidance_capacity(self, professor_id):
        try:
            with open('data/users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            for user in users:
                if user['user_id'] == professor_id and user['role'] == 'professor':
                    return {
                        'capacity': user['capacity_guidance'],
                        'current': user['current_guidance'],
                        'remaining': user['capacity_guidance'] - user['current_guidance']
                    }
            return None
        except:
            return None
