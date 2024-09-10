############################################
# Read .ics file
# convert into df and save in .db
# organize event as the class in courseBot
# ------------------------------------------
# for 'today'
# fetech all events, add into class and run 
# ------------------------------------------
############################################

from icalendar import Calendar
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
import os


# create engine and base globally
Base = declarative_base()

# create tables
class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True)
    class_name = Column(String)
    description = Column(String)
    class_link = Column(String)

    TimeTable = relationship('TimeTable', back_populates='course')


class TimeTable(Base):
    __tablename__ = "TimeTable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(String, ForeignKey("courses.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    course = relationship('Course', back_populates='TimeTable')

Course.TimeTable = relationship('TimeTable', order_by=TimeTable.id, back_populates='course')


# read ics file and save as txt and db file
def read_ics_file():
    print("start reading ics file...")
    with open("Calendar.ics", "r") as f:  
        calendar = f.read()
        
    # save raw ics in txt
    with open("Calendar.txt", "w") as f:
        f.write(str(calendar))

    calendar = Calendar.from_ical(calendar)
    
    engine = create_engine(f"sqlite:///calendar.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # add course into database
    for component in calendar.walk():
        if component.name == "VEVENT":  
            class_name = component.get('SUMMARY')   
            class_start = component.get('DTSTART').dt 
            class_end = component.get('DTEND').dt
            class_description = component.get('DESCRIPTION')
            ### class id format: 1111111-2222 -> also some course starts with letters
            ### here we use the digits before the last hyphen as class_id
            class_id = class_name[-12:-5] 

            # Check if a course already exists
            existing_course = session.query(Course).filter_by(id=class_id).first()

            if existing_course is None:
                new_course = Course(id=class_id, class_name=class_name, description=class_description, class_link=None)
                session.add(new_course)
                session.commit() 
                
            ### for timetable we don't need to check, each record represents a different class time
            ### the time is 4 hours ahead of the real time
            start_time = class_start + datetime.timedelta(hours=4)
            end_time = class_end + datetime.timedelta(hours=4)
            new_TimeTable = TimeTable(class_id=class_id, start_time=start_time, end_time=end_time)
            session.add(new_TimeTable)
            session.commit()
    session.commit()
    session.close()
    print("ics file read and saved in db.")


# load db file and fetch today's classes
def today_table():
    # print("Looking for today's classes...")
    db_name = "calendar"    
    engine = create_engine(f"sqlite:///{db_name}.db")

    current_date = datetime.datetime.now().date()
    Session = sessionmaker(bind=engine)
    session = Session()

    # fetch the class start at current date
    # convert start_time to date format
    today_classes = session.query(TimeTable).filter(func.date(TimeTable.start_time) == current_date).all()
    results = []   
    
    for class_ in today_classes:
        course = session.query(Course).filter(Course.id == class_.class_id).first()
        # print(f"{course.class_name} will start at {class_.start_time}.")
        results.append([course.class_name, course.class_link, class_.start_time, class_.end_time])

    session.close()
    return results



# add online meeting link to exsiting class
def add_link(class_id, link):
    db_name = "calendar.db"
    engine = create_engine(f"sqlite:///{db_name}")
    Session = sessionmaker(bind=engine)
    session = Session()

    class_ = session.query(Course).filter(Course.id == class_id).first()
    if class_:
        class_.class_link = link
        session.commit()
        print(f"Link added to {class_id}: {link}")  
    else:
        print(f"Class {class_id} not found.") 

    session.close()



def db_exsiting_check():
    if os.path.exists("calendar.db"):
        return True
    elif os.path.exists("Calendar.ics"):
        print(f"Loading your ics file...")
        read_ics_file()
        return True
    else:
        print(f"Make sure you have at least save your ics file in the dir.")
        return False



def print_today():
    today_class_list = today_table()
    for course in today_class_list:
        print(f"{course[0]} will start at {course[2]}.")
    print("--------------------------------------------------")
    print(f"You have {len(today_class_list)} classes today. \n \
              Good luck! :p")

def print_all():
    db_name = "calendar"    
    engine = create_engine(f"sqlite:///{db_name}.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    all_classes = session.query(Course).all()
    for class_ in all_classes:
        print(f"COURSE NAME: {class_.class_name} \n \
                COURSE id: {class_.id} \n \
                COURSE LINK: {class_.class_link} \n \n")
    print("--------------------------------------------------")
    print(f"You registered {len(all_classes)} classes now. \n\
               QwQ.")

    session.close()