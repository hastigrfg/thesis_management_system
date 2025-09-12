import json
from ..models.user import Student, Professor, ExternalEvaluator

class AuthService:
    def __init__(self, users_file="data/users.json"):
        self.users_file = users_file
        self.users = self.load_users()
    
    def load_users(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                users_data = json.load(file)
            
            users = {}
            for user_data in users_data:
                if user_data["role"] == "student":
                    users[user_data["user_id"]] = Student(
                        user_data["user_id"], 
                        user_data["name"], 
                        user_data["password"]
                    )
                elif user_data["role"] == "professor":
                    users[user_data["user_id"]] = Professor(
                        user_data["user_id"], 
                        user_data["name"], 
                        user_data["password"],
                        user_data.get("capacity_guidance", 5),
                        user_data.get("capacity_evaluation", 10)
                    )
                elif user_data["role"] == "external_evaluator":
                    users[user_data["user_id"]] = ExternalEvaluator(
                        user_data["user_id"], 
                        user_data["name"], 
                        user_data["password"],
                        user_data.get("capacity_evaluation", 10),  
                        user_data.get("current_evaluation", 0)
                    )    
            return users
        except FileNotFoundError:
            return {}
    
    def login(self, user_id, password):
        user = self.users.get(user_id)
        if user and user.password == password:  
            return user
        return None
    
    def change_password(self, user_id, old_password, new_password):
        user = self.users.get(user_id)
        if user and user.password == old_password:  
            user.password = new_password  
            self.save_users()
            return True
        return False
    
    def save_users(self):
        users_data = []
        for user in self.users.values():
            if user.get_role() == "student":
                users_data.append({
                    "user_id": user.user_id,
                    "name": user.name,
                    "password": user.password,
                    "role": "student"
                })
            elif user.get_role() == "professor":
                users_data.append({
                    "user_id": user.user_id,
                    "name": user.name,
                    "password": user.password,
                    "role": "professor",
                    "capacity_guidance": user.capacity_guidance,
                    "capacity_evaluation": user.capacity_evaluation,
                    "current_guidance": user.current_guidance,
                    "current_evaluation": user.current_evaluation
                })
            elif user.get_role() == "external_evaluator":
                users_data.append({
                    "user_id": user.user_id,
                    "name": user.name,
                    "password": user.password,
                    "role": "external_evaluator",
                    "capacity_evaluation": user.capacity_evaluation,
                    "current_evaluation": user.current_evaluation
                })
        
        with open(self.users_file, 'w', encoding='utf-8') as file:
            json.dump(users_data, file, ensure_ascii=False, indent=4)
    def get_user(self, user_id):
        return self.users.get(user_id)
    def load_users(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                users_data = json.load(file)
            
            users = {}
            for user_data in users_data:
                if user_data["role"] == "student":
                    users[user_data["user_id"]] = Student(
                        user_data["user_id"], user_data["name"], user_data["password"]
                    )
                elif user_data["role"] == "professor":
                    users[user_data["user_id"]] = Professor(
                        user_data["user_id"], user_data["name"], user_data["password"],
                        user_data.get("capacity_guidance", 5),
                        user_data.get("capacity_evaluation", 10),
                        user_data.get("current_guidance", 0),
                        user_data.get("current_evaluation", 0)
                    )
                elif user_data["role"] == "external_evaluator":
                    users[user_data["user_id"]] = ExternalEvaluator(
                        user_data["user_id"], user_data["name"], user_data["password"],
                        user_data.get("capacity_evaluation", 15),
                        user_data.get("current_evaluation", 0)
                    )
            return users
        except FileNotFoundError:
            return {}
