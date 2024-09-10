# online_course_bot

This is a bot that helps me join scheduled online course meetings (especially those at 8:00 in the morning 😒).

## How to use the bot:

### 1. Clone the repository to your local folder

### 2. Create new py env and install the requirements.txt

### 3. Download your calendar and move the `.ics` file (named "calendar.ics") to the same folder

[Instruction link](https://studentuef.sharepoint.com/sites/PeppiHandbook/SitePages/Lukkarikone-Schedule-Assistant.aspx)

### 4. Add the online meeting link to the courses

### 5. Run the `courseBot.py` file

### Other notes:

1. Ensure that when you open the Zoom link in your browser, it automatically opens the Zoom software and joins the meeting. Log in to your Zoom account in advance if needed.

2. Update your calendar `.ics` file when necessary. For example, the maximum period I can download from my calendar is one month, so I need to download and replace the old `.ics` file once a month.

3. The calendar `.ics` file should be named "calendar.ics".

4. You can also edit the .db directly by terminal:  sqlite3 .\calendar.db

5. For Windows, you can set your PC to automatically switch on at a specific time, then add the `.py` script to the Task Scheduler. For example, if your class starts at 8:00 AM, set your PC to automatically switch on at 7:55 AM, and either wake up to the call of fresh knowledge, or sleep tight with it... 😴


# An easier way for IOS users with regular meetings:

use the shortcut app to create an automation with Zoom app action: join the meeting 

-> Enter zoom ID and password

-> Set a weekly or daily schedule    

-> Optional: Laughing at me who spent days writing this and created automation in 2 minutes :(




