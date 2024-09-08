from courseBot import courseBot
import read_calendar as rc
import time





# ------------run the program------------------
example_bot = courseBot()

if rc.db_exsiting_check():
    courseBot.this_cannot_be_UI()
    '''
    rc.add_link("Introduction to Algorithmic Data Analysis (International Students) (JADe) 3621431-3012", \
       "https://uef.zoom.us/j/67113639734?pwd=vQBa58FcC1i4dPtaVdEA0bAPyJ80Gg.1")
    '''

    example_bot.run()



