import schedule
import time
import webbrowser
import read_calendar as rc
import datetime

current_date = time.strftime("%Y-%m-%d", time.localtime())

def open_link(self, link, specific_date = None):
    webbrowser.open(link)

def join_class():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    today_class_list = rc.today_table()

    for course in today_class_list:
        ### couse -> [course.class_name, course.class_link, class_.start_time, class_.end_time]
        # print(f"{course[0]} will start at {course[2]}.")
        ### convert start_time to same format as current_time
        start_time = datetime.datetime.strftime(course[2], "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strftime(course[3], "%Y-%m-%d %H:%M:%S")
        if current_time >= start_time and current_time <= end_time:
            open_link(course[1])
            break
    # print("join def end here")

### class object
class course:
    def __init__(self, course_name, link, start_date, end_date, start_time, end_time):
        self.course_name = course_name
        self.link = link
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time 


def run():
    print(f"Today is {current_date}. :)")
    if rc.db_exsiting_check():
        rc.print_today()
    print("I'm still running... e_e...")
    while True:
        join_class()
        time.sleep(5)


# add zoom link to exsiting class
def add_link(self, course_name, link):
    rc.add_link(course_name, link)
        

    
    # TODO:update functions to use the UI add and modify courses. 
def this_cannot_be_UI():
    print("Welcome to use courseBot: \n \
              Enter 1 to check today's class;\n \
              Enter 2 to print all the classes with online meeting link;\n \
              Enter 3 to add new course;\n \
              Enter 4 to modify exsiting course;\n \
              Enter q to quit.\n ")
        

# ------------run the program------------------
if __name__ == "__main__":
    # courseBot.this_cannot_be_UI()

    run()
