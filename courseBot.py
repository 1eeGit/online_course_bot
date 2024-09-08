import schedule
import time
import webbrowser
import read_calendar as rc

current_date = time.strftime("%Y-%m-%d", time.localtime())

def open_link(self, link, specific_date = None):
    webbrowser.open(link)

def join_class():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    courses = {}

    today_classes = rc.today_table()

    for course in today_classes:
        print(course)
        course_obj = course(course.class_name, course.class_link, course.start_date, course.end_date, course.start_time, course.end_time)
        courses[course.class_name] = course_obj
    
    for course in courses:
        if current_time >= course.start_time and current_time <= course.end_time:
            open_link(courses[course].link)
            break

### class object
class course:
    def __init__(self, course_name, link, start_date, end_date, start_time, end_time):
        self.course_name = course_name
        self.link = link
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time 

### courseBot object
class courseBot:
    def __init__(self):
        self.schedule = schedule


    def clear_all(self):
        self.schedule.clear()

    def run(self):
        while True:
            join_class()
            time.sleep(1)




    # add zoom link to exsiting class
    def add_link(self, course_name, link):
        rc.add_link(course_name, link)
        

    
    # TODO:
    # add function to use the UI add and modify courses. 
    def this_cannot_be_UI():
        print("Welcome to use courseBot: \n \
              Enter 1 to check today's class;\n \
              Enter 2 to print all the classes with online meeting link;\n \
              Enter 3 to add new course;\n \
              Enter 4 to modify exsiting course;\n \
              Enter q to quit.\n ")
        

            