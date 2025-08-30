import json
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = password
    
    @abstractmethod
    def get_role(self):
        pass
    
    def verify_password(self, password):
        return self.password == password
    
    def change_password(self, new_password):
        self.password = new_password
        return True

class Student(User):
    def get_role(self):
        return "student"
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password,
            "role": self.get_role()
        }

class Professor(User):
    def __init__(self, user_id, name, password, capacity_guidance=5, capacity_evaluation=10, current_guidance=0, current_evaluation=0):
        super().__init__(user_id, name, password)
        self.capacity_guidance = capacity_guidance
        self.capacity_evaluation = capacity_evaluation
        self.current_guidance = current_guidance
        self.current_evaluation = current_evaluation
    
    def get_role(self):
        return "professor"
    
    def can_accept_guidance(self):
        return self.current_guidance < self.capacity_guidance
    
    def can_accept_evaluation(self):
        return self.current_evaluation < self.capacity_evaluation
    
    def add_guidance(self):
        if self.can_accept_guidance():
            self.current_guidance += 1
            return True
        return False
    
    def remove_guidance(self):
        if self.current_guidance > 0:
            self.current_guidance -= 1
            return True
        return False
    
    def add_evaluation(self):
        if self.can_accept_evaluation():
            self.current_evaluation += 1
            return True
        return False
    
    def remove_evaluation(self):
        if self.current_evaluation > 0:
            self.current_evaluation -= 1
            return True
        return False
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password,
            "role": self.get_role(),
            "capacity_guidance": self.capacity_guidance,
            "capacity_evaluation": self.capacity_evaluation,
            "current_guidance": self.current_guidance,
            "current_evaluation": self.current_evaluation
        }

class ExternalEvaluator(User):
    def __init__(self, user_id, name, password, capacity_evaluation=10, current_evaluation=0):  # تغییر از 15 به 10
        super().__init__(user_id, name, password)
        self.capacity_evaluation = capacity_evaluation
        self.current_evaluation = current_evaluation
    
    def get_role(self):
        return "external_evaluator"
    
    def can_accept_evaluation(self):
        return self.current_evaluation < self.capacity_evaluation
    
    def add_evaluation(self):
        if self.can_accept_evaluation():
            self.current_evaluation += 1
            return True
        return False
    
    def remove_evaluation(self):
        if self.current_evaluation > 0:
            self.current_evaluation -= 1
            return True
        return False
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password,
            "role": self.get_role(),
            "capacity_evaluation": self.capacity_evaluation,
            "current_evaluation": self.current_evaluation
        }
