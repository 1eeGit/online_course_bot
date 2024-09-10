import time
import webbrowser
import read_calendar as rc
import datetime

current_date = time.strftime("%Y-%m-%d", time.localtime())

def open_link(link):
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
            if course[1]:
                print(f"Joining... \n \
                      {course[0]} ... \n ")
                print(f"Link: {course[1]}")
                open_link(course[1])
            else: 
                print(f"{course[0]} is starting now. But no link is provided.")
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
    while True:
        join_class()
        time.sleep(5)
        this_cannot_be_UI(ask_user())
        time.sleep(5)
        print("I'm still running... you're welcome...")
        

# add zoom link to exsiting class
def add_link(course_id, link):
    rc.add_link(course_id, link)
        
def ask_user():
    user_input = input()
    return user_input
    
def this_cannot_be_UI(user_input = None):
    valid_input = ["1", "2", "3", "r", "q"]
    if user_input not in valid_input:
        print("I don't understand what you are talking about. \n \
              @#$%^&*)_(*&^%$#@!@#$%^&*")
        this_cannot_be_UI(ask_user())
    else:
        match user_input:
            case "1":
                rc.print_today()
                this_cannot_be_UI(ask_user())
            case "2":
                rc.print_all()
                this_cannot_be_UI(ask_user())
            case "3":
                course_id = input("Enter the course id:  \n \
                    (you can find it by entering 2 to print all the classes.) \n") 
                link = input("Enter the link: ")
                if link == None:
                    print("Link cannot be empty.")
                    this_cannot_be_UI(ask_user())
                else: add_link(course_id, link)
                this_cannot_be_UI(ask_user())
            case "r":
                run()
            case "q":
                print("Powering off...")
                exit()
        

# ------------run the program------------------
if __name__ == "__main__":
    print("Welcome to use courseBot: \n \
              Enter 1 to check today's class;\n \
              Enter 2 to print all the classes;\n \
              Enter 3 to add/ edit meeting link;\n \
              Enter r to run the bot;\n \
              Enter q to quit.\n ")
    print(f"Today is {current_date}. :)")
    if rc.db_exsiting_check():
        this_cannot_be_UI(ask_user())
    
    

