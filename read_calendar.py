# export ics file, save in the same folder with the codes
# https://studentuef.sharepoint.com/sites/PeppiHandbook/SitePages/Lukkarikone-Schedule-Assistant.aspx

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



def read_ics_file(file_path, csv_name):
    with open(file_path, "r") as f:  
        calendar = f.read()
        
    # save raw ics in txt
    with open(f"{csv_name}.txt", "w") as f:
        f.write(str(calendar))

    calendar = Calendar.from_ical(calendar)
    df = pd.DataFrame(columns=["Class_name", "Start_time", "End_time", "Description"])

    engine = create_engine(f"sqlite:///{csv_name}.db")
    Base = declarative_base()

    # create table: courses, timetable
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
            new_timeTable = timeTable(class_id=new_course.id, start_time=event_start, end_time=event_end)

            session.add(new_course)
            session.add(new_timeTable)
            session.commit()

            # df.loc[len(df)] = [event_name, event_start, event_end, event_description]
    

    # df.to_csv(f"{csv_name}.csv")



# ------------------------------
read_ics_file("calendar_week1.ics", "calendar_week1_df")

