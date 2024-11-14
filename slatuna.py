import datetime as dt, time as t, json as j, os, psutil,sys,threading
from PIL import Image
from pygame import mixer
from database import main as database
from stray import main as tray_icon

#  https://www.mediafire.com/file/3kidit35e811cj0/Slatuna.zip/file
p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)  # أو استخدم psutil.REALTIME_PRIORITY_CLASS لزيادة الأولوية إلى الحد الأقصى

loc = os.path.dirname(__file__)
os.chdir(loc)

check = threading.Thread(target= lambda: database())
check.start()
check.join()

tray = threading.Thread(target= lambda: tray_icon())
tray.start()

def JsonFile():
    with open(f"{loc}/assets/data/database.json", "r") as file:
        return j.load(file)
fileopend = JsonFile()

def save_json_data(data):
    with open(f"{loc}/assets/data/database.json", "w") as file:
       j.dump(data, file, indent=4)

def get_time_in_minutes(time_str):
    time_obj = dt.datetime.strptime(time_str, "%H:%M").time()
    return dt.timedelta(hours=time_obj.hour, minutes=time_obj.minute)

all_pray = fileopend["sys"]["times"][0]["all_times"]
all_times = fileopend["sys"]["times"][0]["all_times_during"]

all_times_now = t.strftime("%p")
time_befor = dt.timedelta(minutes=5)

prayer_times = [get_time_in_minutes(pray) for pray in all_pray]
time_before_prayers = [time - time_befor for time in prayer_times]

loop = True

while loop:
    print("im here")
    current_time_str = t.strftime("%H:%M")
    current_time = get_time_in_minutes(current_time_str)

    for i, (prayer_time, time_before_prayer) in enumerate(zip(prayer_times, time_before_prayers)):
        print(current_time,prayer_time,time_before_prayer)
        if current_time == prayer_time and all_times[i] == all_times_now:
            print(f"Current time matches prayer time for prayer {i}")
            mixer.init()  # pygame mixer
            alarm = mixer.Sound(f"{loc}/assets/Voices/aa.mp3")  # define the voice to pygame
            alarm.play()  # play mixer

            #r = subprocess.run([f"{loc}/the_remainder.exe"], check=True, capture_output=True, text=True)

            os.startfile("database.exe")

            #repeted -=1
            t.sleep(60)
        elif current_time == time_before_prayer and all_times[i] == all_times_now:
            print(f"Current time matches time before prayer for prayer {i}")
            mixer.init()  # pygame mixer
            alarm = mixer.Sound(f"{loc}/assets/Voices/bf.mp3")  # define the voice to pygame
            alarm.play()  # play mixer
            #repeted +=1
            t.sleep(60)
    t.sleep(25)