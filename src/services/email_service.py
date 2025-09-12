import json
from datetime import datetime
import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.email import Email
from config import EMAILS_FILE, USERS_FILE

class EmailService:
    def __init__(self, emails_file=EMAILS_FILE, users_file=USERS_FILE):
        self.emails_file = emails_file
        self.users_file = users_file
        self.emails = self.load_emails()
        self.users = self.load_users()
    
    def load_emails(self):
        
        try:
            with open(self.emails_file, 'r', encoding='utf-8') as file:
                emails_data = json.load(file)
                return [Email.from_dict(data) for data in emails_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def load_users(self):
       
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_emails(self):
        
        emails_data = [email.to_dict() for email in self.emails]
        with open(self.emails_file, 'w', encoding='utf-8') as file:
            json.dump(emails_data, file, ensure_ascii=False, indent=4)
    
    def get_user_by_email(self, email):
      
        for user in self.users:
            if user.get('email') == email:
                return user
        return None
    
    def get_user_by_id(self, user_id):
       
        for user in self.users:
            if user.get('user_id') == user_id:
                return user
        return None
    
    def send_email(self, sender_email, receiver_email, subject, content, attachments=None):
        
        try:
            
            sender = self.get_user_by_email(sender_email)
            receiver = self.get_user_by_email(receiver_email)
            
            if not sender:
                return False, "ایمیل فرستنده معتبر نیست"
            if not receiver:
                return False, "ایمیل گیرنده معتبر نیست"
            
            email_id = f"email_{len(self.emails) + 1}_{int(datetime.now().timestamp())}"
            
            new_email = Email(
                email_id=email_id,
                sender_email=sender_email,
                receiver_email=receiver_email,
                subject=subject,
                content=content
            )
            if attachments:
                for attachment in attachments:
                    new_email.add_attachment(attachment['name'], attachment['path'])
            
            self.emails.append(new_email)
            self.save_emails()
            
            return True, "ایمیل با موفقیت ارسال شد"
            
        except Exception as e:
            return False, f"خطا در ارسال ایمیل: {str(e)}"
    
    def get_inbox(self, user_email, unread_only=False, label_filter=None):
        try:
            inbox_emails = []
            for email in self.emails:
                if email.receiver_email == user_email and not email.is_archived:
                    if unread_only and email.is_read:
                        continue
                    if label_filter and label_filter not in email.labels:
                        continue
                    inbox_emails.append(email)
            inbox_emails.sort(key=lambda x: x.timestamp, reverse=True)
            return inbox_emails
            
        except Exception as e:
            print(f"خطا در دریافت inbox: {e}")
            return []
    
    def get_sent_emails(self, user_email):
       
        try:
            sent_emails = [email for email in self.emails if email.sender_email == user_email]
            sent_emails.sort(key=lambda x: x.timestamp, reverse=True)
            return sent_emails
        except Exception as e:
            print(f"خطا در دریافت ایمیل‌های ارسال شده: {e}")
            return []
    
    def get_archived_emails(self, user_email):
        
        try:
            archived_emails = [email for email in self.emails 
                             if email.receiver_email == user_email and email.is_archived]
            archived_emails.sort(key=lambda x: x.timestamp, reverse=True)
            return archived_emails
        except Exception as e:
            print(f"خطا در دریافت ایمیل‌های آرشیو شده: {e}")
            return []
    
    def mark_as_read(self, email_id, user_email):
        
        try:
            for email in self.emails:
                if email.email_id == email_id and email.receiver_email == user_email:
                    email.mark_as_read()
                    self.save_emails()
                    return True, "ایمیل خوانده شد"
            return False, "ایمیل یافت نشد"
        except Exception as e:
            return False, f"خطا در بروزرسانی ایمیل: {str(e)}"
    
    def archive_email(self, email_id, user_email):
      
        try:
            for email in self.emails:
                if email.email_id == email_id and email.receiver_email == user_email:
                    email.archive()
                    self.save_emails()
                    return True, "ایمیل آرشیو شد"
            return False, "ایمیل یافت نشد"
        except Exception as e:
            return False, f"خطا در آرشیو ایمیل: {str(e)}"
    
    def search_emails(self, user_email, query):
       
        try:
            results = []
            for email in self.emails:
                if email.receiver_email == user_email:
                    if (query.lower() in email.subject.lower() or 
                        query.lower() in email.content.lower() or
                        query.lower() in email.sender_email.lower()):
                        results.append(email)
            
            results.sort(key=lambda x: x.timestamp, reverse=True)
            return results
        except Exception as e:
            print(f"خطا در جستجو: {e}")
            return []
    
    def get_email_stats(self, user_email):
       
        try:
            total = len([e for e in self.emails if e.receiver_email == user_email])
            unread = len([e for e in self.emails if e.receiver_email == user_email and not e.is_read])
            archived = len([e for e in self.emails if e.receiver_email == user_email and e.is_archived])
            
            return {
                'total': total,
                'unread': unread,
                'archived': archived,
                'read': total - unread
            }
        except Exception as e:
            print(f"خطا در محاسبه آمار: {e}")
            return {'total': 0, 'unread': 0, 'archived': 0, 'read': 0}
