from customtkinter import *
import keyboard,mouse, json as j,os,sys,win32.win32gui as win32gui,win32.lib.win32con as win32con,ctypes,psutil

the_pid = os.getpid()

p = psutil.Process(the_pid)
p.nice(psutil.REALTIME_PRIORITY_CLASS)  # أو استخدم psutil.REALTIME_PRIORITY_CLASS لزيادة الأولوية إلى الحد الأقصى

#location = os.path.dirname(sys.executable)  # عند تشغيل البرنامج كملف .py
location = os.path.dirname(__file__)  # عند تشغيل البرنامج كملف .exe

def load_json_file():
    try:
        with open(f"{location}/assets/data/database.json", "r") as thefile:
            return j.load(thefile)
    except (j.decoder.JSONDecodeError,FileNotFoundError):
        initial_data = {
                        "sys": {
                            "year": "1",
                            "month": "",
                            "day": "",
                            "version": "",
                            "pid": "",
                            "times": []
                        }
                    }
        with open(f"{location}/assets/data/database.json", "w") as controler:
            j.dump(initial_data, controler, indent=4)
        return initial_data
fileopend = load_json_file()

def save_json_file(data):
    with open(f"{location}/assets/data/database.json", "w") as f:
        j.dump(data, f, indent=4)

the_label_time = fileopend["sys"]["times"][0]["all_times"] if fileopend["sys"]["times"] else ""

if len(the_label_time) == 6:
    the_label_time = "fajr"
elif len(the_label_time) == 4:
    the_label_time = "dhuhr"
elif len(the_label_time) == 3:
    the_label_time = "asr"
elif len(the_label_time) == 2:
    the_label_time = "maghrib"
else:
    the_label_time = "isha"

root = CTk()
root.title("hi")
root.focus()
root.grab_set()
root.wm_attributes("-topmost", True)
root.wm_attributes("-fullscreen", True)

def make_window_always_on_top():
    print("img here make_window_always_on_top")
    hwnd = win32gui.FindWindow(None, "hi")
    if hwnd:
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOPMOST)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        # Force the window to be on top of full-screen applications
        ctypes.windll.user32.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        ctypes.windll.user32.SetFocus(hwnd)
        root.after(1,make_window_always_on_top)
        root.after(1,root.focus)
# وظيفة للحفاظ على النافذة في المقدمة بشكل مستمر
def keep_window_on_top():
    print("img here keep_window_on_top")
    hwnd = win32gui.FindWindow(None, "hi")
    if hwnd:
        ctypes.windll.user32.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    root.after(1, keep_window_on_top)  # إعادة التحقق كل ثانية
    root.after(1,root.focus)

def go_ya_mouse():
    mouse.move(0,0)
    root.after(1,go_ya_mouse)

def qu():
    root.quit()

def disable_always_on_top():
    hwnd = win32gui.FindWindow(None, "Task Manager")
    if hwnd:
        # إزالة نمط "Always on Top"
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_TOPMOST)
        # تحديث النافذة لتعكس التغيير
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
    root.after(1,disable_always_on_top)

keyboard.block_key("f4")
keyboard.block_key("tab")
keyboard.block_key("t")
keyboard.add_hotkey("ctrl+a+j",qu)

go_ya_mouse()
make_window_always_on_top()
keep_window_on_top()
disable_always_on_top()

root.after(900000,qu)

go_pray = CTkLabel(master=root, text="Go Pray", font=("Cairo", 30))
go_pray.pack(anchor="center")

the_slah_remainder = CTkLabel(master=root, text="Slat El " + str(the_label_time), font=("Cairo", 40))
the_slah_remainder.pack(anchor="center")

the_tkber = CTkLabel(master=root, text="Allahu Akbar", font=("Cairo", 50))
the_tkber.pack(anchor="center")

root.mainloop()