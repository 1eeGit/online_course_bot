############################################
# Read ics file
# convert into df and save in csv/ db
# organize event as the class in courseBot
# ------------------------------------------
# for 'today'
# fetech all events, add into class and run 
# ------------------------------------------
############################################

from icalendar import Calendar
import datetime
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os


# create engine and base globally
Base = declarative_base()

# create tables
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    class_name = Column(String)
    description = Column(String)
    class_link = Column(String)


class timeTable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("courses.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    course = relationship('Course', back_populates='timetable')

Course.timetable = relationship('timeTable', order_by=timeTable.id, back_populates='course')


# read ics file and save as txt and db file
def read_ics_file():
    with open("Calendar.ics", "r") as f:  
        calendar = f.read()
        
    # save raw ics in txt
    with open("Calendar.txt", "w") as f:
        f.write(str(calendar))

    calendar = Calendar.from_ical(calendar)
    df = pd.DataFrame(columns=["Class_name", "Start_time", "End_time", "Description"])

    engine = create_engine(f"sqlite:///calendar.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # add course into database
    for component in calendar.walk():
        if component.name == "VEVENT":  
            event_name = component.get('SUMMARY')   
            event_start = component.get('DTSTART').dt 
            event_end = component.get('DTEND').dt
            event_description = component.get('DESCRIPTION')

            new_course = Course(class_name=event_name, description=event_description, class_link="")
            session.add(new_course)
            session.commit()

            new_timeTable = timeTable(class_id=new_course.id, start_time=event_start, end_time=event_end)
            session.add(new_timeTable)
            session.commit()
    session.commit()
    session.close()




# load db file and fetch today's classes
# TODO:
# Looking for Course with class_id: None
# Warning: No course found for class_id None
#     course_obj = course(course.class_name, course.class_link, course.start_date, course.end_date, course.start_time, course.end_time)
# AttributeError: 'timeTable' object has no attribute 'class_name'
def today_table():
    db_name = "calendar"    
    engine = create_engine(f"sqlite:///{db_name}.db")

    current_date = datetime.datetime.now().date()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch all classes that are scheduled for today
    today_classes = session.query(timeTable).filter(timeTable.start_time >= current_date).all()

    for class_ in today_classes:
        print(f"Looking for Course with class_id: {class_.class_id}")
        course = session.query(Course).filter(Course.id == class_.class_id).first()

        if course:
            print(f"Class: {course.class_name}, Start: {class_.start_time}")
        else:
            print(f"Warning: No course found for class_id {class_.class_id}")

    session.close()
    return today_classes



# add online meeting link to exsiting class
def add_link(class_name, link):
    db_name = "calendar.db"
    engine = create_engine(f"sqlite:///{db_name}")
    Session = sessionmaker(bind=engine)
    session = Session()

    class_ = session.query(Course).filter(Course.class_name == class_name).first()
    if class_:
        class_.class_link = link
        session.commit()
        print(f"Link added to {class_name}: {link}")  
    else:
        print(f"Class {class_name} not found.") 

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

