import schedule
import time
import webbrowser

current_date = time.strftime("%Y-%m-%d", time.localtime())

def open_link(self, link, specific_date = None):
    webbrowser.open(link)

def join_class(link, weekday, time):
    schedule.every().weekday.at(time).do(open_link(link))

class courseBot:
    def __init__(self):
        self.schedule = schedule
        self.start_date = None
        self.end_date = None

    def clear_all(self):
        self.schedule.clear()

    def run(self):
        while self.start_date < current_date < self.end_date:
            self.schedule.run_pending()
            time.sleep(1)
        self.clear_all()

    def add_check(self, link, weekday, class_time, exception_date, replacement_date):
        weekdays = {'monday': self.schedule.every().monday, 
                    'tuesday': self.schedule.every().tuesday, 
                    'wednesday': self.schedule.every().wednesday, 
                    'thursday': self.schedule.every().thursday, 
                    'friday': self.schedule.every().friday, 
                    'saturday': self.schedule.every().saturday, 
                    'sunday': self.schedule.every().sunday}
        
        ### job is not callable error
        self.schedule.every().tuesday.at(class_time).do(open_link, link)
        '''
        if weekday.lower() in weekdays:
            if exception_date and replacement_date:
                replacement_date_obj = time.strptime(replacement_date, "%Y-%m-%d")
                exception_date_obj = time.strptime(exception_date, "%Y-%m-%d")

                self.schedule.every().day.at(class_time).do(self.open_link, link, replacement_date_obj).tag(replacement_date)
                weekdays[weekday.lower()]().at(class_time).do(self.open_link, link, exception_date_obj).tag(weekday)
            else:
                weekdays[weekday.lower()]().at(class_time).do(open_link, link)
        else:
            print("Invalid weekday for course on " + weekday)
        '''

    # exception and replacement date format: "%Y-%m-%d"
    def add_class(self, link, weekday, class_time, start_date, end_date, exception_date = None, replacement_date = None):
        self.start_date = start_date
        self.end_date = end_date
        if start_date < current_date < end_date:
            self.add_check(link, weekday, class_time, start_date, end_date, exception_date, replacement_date)
        else:
            print("Course " + self + " is not ongoing")

            