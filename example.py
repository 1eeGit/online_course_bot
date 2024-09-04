from courseBot import courseBot
import time

'''example : Mondays 08:00–10:00
Thursdays 08:00–10:00
from Monday 9 September to Thursday 24 October
Exceptions:
Friday 20 September replaces Monday 23 September
Wednesday 2 October replaces Thursday 26 September'''

example_link = "your_test_link_here"
example_bot = courseBot()

example_bot.add_class(example_link, "Monday", "08:00", "2024-09-09", "2024-10-24", "2024-09-24", "2024-09-09")
example_bot.add_class(example_link, "Thursday", "08:00", "2024-09-09", "2024-10-24", "2024-09-26", "2024-10-02")

example_bot.run()
