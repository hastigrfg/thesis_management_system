class Course:
    def __init__(self, course_id, title, professor_id, year, semester, 
                 capacity, resources, sessions, units, current_students=0):
        self.course_id = course_id
        self.title = title
        self.professor_id = professor_id
        self.year = year
        self.semester = semester
        self.capacity = capacity
        self.resources = resources
        self.sessions = sessions
        self.units = units
        self.current_students = current_students
    
    def has_capacity(self):
        return self.current_students < self.capacity
    
    def add_student(self):
        if self.has_capacity():
            self.current_students += 1
            return True
        return False
    
    def remove_student(self):
        if self.current_students > 0:
            self.current_students -= 1
            return True
        return False
    
    def to_dict(self):
        return {
            "course_id": self.course_id,
            "title": self.title,
            "professor_id": self.professor_id,
            "year": self.year,
            "semester": self.semester,
            "capacity": self.capacity,
            "current_students": self.current_students,
            "resources": self.resources,
            "sessions": self.sessions,
            "units": self.units
        }
