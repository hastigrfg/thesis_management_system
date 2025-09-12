import json
from datetime import datetime
from config import THESES_FILE, THESIS_REQUESTS_FILE

class ReportService:
    def __init__(self):
        self.theses_file = THESES_FILE
        self.thesis_requests_file = THESIS_REQUESTS_FILE
    
    def generate_professor_report(self, professor_id, start_date=None, end_date=None):
        try:
            with open(self.theses_file, 'r', encoding='utf-8') as f:
                theses = json.load(f)
            
            with open(self.thesis_requests_file, 'r', encoding='utf-8') as f:
                thesis_requests = json.load(f)
            
            
            professor_theses = [t for t in theses if t['professor_id'] == professor_id]
            professor_requests = [r for r in thesis_requests if r['professor_id'] == professor_id]
            
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                
                professor_theses = [t for t in professor_theses 
                                  if start_date <= datetime.strptime(t['completion_date'], '%Y-%m-%d %H:%M:%S') <= end_date]
                professor_requests = [r for r in professor_requests 
                                    if start_date <= datetime.strptime(r['request_date'], '%Y-%m-%d %H:%M:%S') <= end_date]
            
            
            report = {
                'period': f"{start_date} to {end_date}" if start_date and end_date else 'All time',
                'total_students': len(set(t['student_id'] for t in professor_theses)),
                'completed_theses': len(professor_theses),
                'average_score': self._calculate_average_score(professor_theses),
                'approval_rate': self._calculate_approval_rate(professor_requests),
                'grade_distribution': self._calculate_grade_distribution(professor_theses),
                'timeline_data': self._generate_timeline_data(professor_theses),
                'student_performance': self._generate_student_performance(professor_theses)
            }
            
            return {'success': True, 'report': report}
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _calculate_average_score(self, theses):
        scores = [t['final_score'] for t in theses if t['final_score'] is not None]
        return round(sum(scores) / len(scores), 2) if scores else 0
    
    def _calculate_approval_rate(self, requests):
        approved = len([r for r in requests if r['status'] == 'approved'])
        total = len(requests)
        return round((approved / total) * 100, 2) if total > 0 else 0
    
    def _calculate_grade_distribution(self, theses):
        grades = {'الف': 0, 'ب': 0, 'ج': 0, 'د': 0}
        for thesis in theses:
            if thesis['final_score'] >= 17:
                grades['الف'] += 1
            elif thesis['final_score'] >= 14:
                grades['ب'] += 1
            elif thesis['final_score'] >= 12:
                grades['ج'] += 1
            else:
                grades['د'] += 1
        return grades
    
    def _generate_timeline_data(self, theses):
        timeline = {}
        for thesis in theses:
            year = thesis['year']
            if year not in timeline:
                timeline[year] = 0
            timeline[year] += 1
        return timeline
    
    def _generate_student_performance(self, theses):
        performance = []
        for thesis in theses:
            performance.append({
                'student_id': thesis['student_id'],
                'score': thesis['final_score'],
                'grade': 'الف' if thesis['final_score'] >= 17 else
                        'ب' if thesis['final_score'] >= 14 else
                        'ج' if thesis['final_score'] >= 12 else 'د'
            })
        return performance
