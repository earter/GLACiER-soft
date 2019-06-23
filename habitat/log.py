import logging
import datetime

now = datetime.datetime.now().strftime('%H:%M:%S')
# f = f"log_{now}.log"
# logging.basicConfig(filename=f, level=logging.DEBUG)

f = open(f"log_{now}.log", "w")

weather_list = ['wd', 'ws', 'wda', 'wsa', 'h', 't', 'r', 'p', 'b']

for item in weather_list:
    f.write(f"{item}\n")

f.close()
