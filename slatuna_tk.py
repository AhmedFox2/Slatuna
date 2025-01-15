import PIL.Image
from customtkinter import *
import os, json, datetime as dt, webbrowser,PIL.Image

# Change directory to the script's location
location = os.path.dirname(__file__)
os.chdir(location)

# Function to load JSON settings file
def Json_file():
    try:
        with open(f"{location}/assets/data/Settings.json", "r") as controler:
            return json.load(controler)
    except FileNotFoundError:
        f = open(f"{location}/assets/data/Settings.json", "r")
    except json.decoder.JSONDecodeError:
        with open(f"{location}/assets/data/Settings.json", "w") as controler:
            ha = {
                    "app": {
                        "apper": "system",
                        "language": "ar"
                    }
                }
            he = '"' 
            controler.write(str(ha).replace("'", he))
            return ha

file_loaded = Json_file()

# Function to save JSON settings file
def save_json_file(data):
    with open(f"{location}/assets/data/Settings.json", "w") as controler:
        json.dump(data, controler, indent=4)

# Translation dictionaries
translations = {
    "en": {
        "title": "Slatuna",
        "settings": "Settings",
        "appearance": "Appearance",
        "dark": "Dark",
        "light": "Light",
        "support": "Support",
        "discord": "Discord",
        "help_text": "If there is any problem please join my Discord server",
        "help_text_2": "and report it 'just press the button below'",
        "prayers": ["Fajer", "Shuruk", "Duher", "Aser", "Magreb", "Asha"]
    },
    "ar": {
        "title": "صلاتنا",

        "settings": "الإعدادات",
        "appearance": "المظهر",
        "dark": "داكن",
        "light": "فاتح",

        "support": "الدعم",
        "discord": "ديسكورد",
        "help_text": "إذا كانت هناك أي مشكلة، يرجى الانضمام إلى خادم الديسكورد",
        "help_text_2": "والإبلاغ عنها 'اضغط على الزر أدناه'",

        "prayers": ["الفجر", "الشروق", "الظهر", "العصر", "المغرب", "العشاء"],
        
        "Friday": "الجمعة",
        "Thursday":"الخميس",
        "Wednesday":"الأربعاء",
        "Tuesday":"الثلاثاء",
        "Monday":"الأثنين",
        "Sunday":"الأحد",
        "Saturday":"السبت",
        
        "January": "يناير",
        "February": "فبراير",
        "March": "مارس",
        "April": "أبريل",
        "May": "مايو",
        "June": "يونيو",
        "July": "يوليو",
        "August": "أغسطس",
        "September": "سبتمبر",
        "October": "أكتوبر",
        "November": "نوفمبر",
        "December": "ديسمبر",

        "1":"١","2":"٢","3":"٣","4":"٤","5":"٥",
        "6":"٦","7":"٧","8":"٨","9":"٩","10":"١٠",
        "11": "١١", "12": "١٢", "13": "١٣",
          "14": "١٤","15": "١٥",
        "16": "١٦", "17": "١٧", "18": "١٨",
          "19": "١٩", "20": "٢٠",
        "21": "٢١", "22": "٢٢", "23": "٢٣",
          "24": "٢٤", "25": "٢٥",
        "26": "٢٦", "27": "٢٧", "28": "٢٨",
          "29": "٢٩", "30": "٣٠",
        "31": "٣١"        
}
    }


current_language = file_loaded["app"].get("language", "en")

def translate(text_key):
    return translations[current_language].get(text_key, text_key)

def main():
    # Initialize the main window
    root = CTk()
    root.title(translate("title"))
    icon = PIL.Image.open(f"{location}/assets/Imgs/icon2.png")
    root.wm(False,CTk(light_image=icon,dark_image=icon))

    # Set the window size and position
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    app_w = 330
    app_h = 330
    x = (screen_w / 2) - (app_w / 2)
    y = (screen_h / 2) - (app_h / 2)
    root.geometry(f"{app_w}x{app_h}+{int(x)}+{int(y)}")
    root.resizable(False, False)

    the_apper_is = file_loaded["app"]["apper"]
    set_appearance_mode(the_apper_is)

    def the_database_file():
        with open(f"{location}/assets/data/database.json", "r") as the_database_file_opened:
            return json.load(the_database_file_opened)
    
    the_database_file_opened = the_database_file()
    all_times = the_database_file_opened["sys"]["times"][0]["all_times_2"]
    
    today = dt.date.today()
    the_orginal_date = today.strftime(r"%A %d %B %Y")
    test = the_orginal_date.split()
    the_date = f"{translate(test[0])} {test[1]} {test[2]} {test[3]}"

    # Set background image
    #background_image = CTkImage("assets/background.jpg")
    #background_label = CTkLabel(root, image=background_image)
    #background_label.place(relwidth=1, relheight=1)

    # Display the current date
    the_date_text = CTkLabel(root, text=the_date, font=("Noto Kufi Arabic", 15))
    the_date_text.place(x=20, y=10)

    # Create a frame for prayer times
    prayer_frame = CTkFrame(root, width=app_w-40, height=app_h-100, bg_color="transparent")
    prayer_frame.place(x=20, y=50)

    # Display prayer times
    prayer_times = []
    for i in range(6):
        result = (translate("prayers")[i], all_times[i])
        prayer_times.append(result)

    for i, (name, time) in enumerate(prayer_times):
        row = i // 3  # Determine the row (3 columns per row)
        column = i % 3  # Determine the column

        frame = CTkFrame(prayer_frame, width=(app_w-60)/3, height=100, fg_color="transparent")
        frame.grid(row=row, column=column, padx=10, pady=10)
        
        label = CTkLabel(frame, text=name, font=("Noto Kufi Arabic", 25), text_color="#95C8D8", bg_color="transparent")
        label.pack(side="top", pady=(10,5))
        
        time_label = CTkLabel(frame, text=time, font=("Noto Kufi Arabic", 25), text_color="white", bg_color="transparent")
        time_label.pack(side="bottom", pady=(5,10))

    # Settings button
    settings_btn = CTkButton(root, width=50, text=translate("settings"), command=lambda: settings(root), border_width=2, border_color="white", fg_color="transparent", corner_radius=50)
    settings_btn.pack(side="bottom",anchor="w",padx=25,pady=20)

    root.mainloop()

def settings(root):

    def write_the_apper():
        the_choise = ld_sw_var.get()
        set_appearance_mode(the_choise)
        ld_sw.configure(text=translate(the_choise))
        file_loaded["app"]["apper"] = str(the_choise)
        save_json_file(file_loaded)
    
    def web():
        webbrowser.open("https://discord.gg/pTbVg78xKd")
 
    def change_language(lang):
        global current_language

        current_language = lang
        file_loaded["app"]["language"] = lang
        save_json_file(file_loaded)

        window.quit()
        window.destroy()

        try:
            root.quit()
            root.destroy()
        except AttributeError:
            pass
        
        main()
                   
    window = CTk()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    app_w = 800
    app_h = 500
    x = (screen_w / 2) - (app_w / 2)
    y = (screen_h / 2) - (app_h / 2)
    window.geometry(f"{app_w}x{app_h}+{int(x)}+{int(y)}")
    window.resizable(False, False)
    window.wm_attributes("-topmost", True)
        
    btn_frame = CTkFrame(window, width=150, height=500, corner_radius=15)
    btn_frame.place(x=0, y=0)
        
    appearance_btn = CTkButton(btn_frame, text=translate("appearance"), corner_radius=15, command=lambda: appearance_frame.tkraise())
    appearance_btn.place(x=4, y=10)

    appearance_frame = CTkFrame(window, width=650, height=500, corner_radius=0)
    appearance_frame.place(x=150, y=0)

    ld_btn = CTkLabel(appearance_frame, text=translate("appearance"), font=("Noto Kufi Arabic", 15))
    ld_btn.place(x=150, y=10)
        
    ld_sw_var = StringVar(value="off")
    ld_sw = CTkSwitch(appearance_frame, corner_radius=50, text=translate("dark"), onvalue="dark", offvalue="light", variable=ld_sw_var, command=write_the_apper)
    ld_sw.place(x=150, y=30)
        
    support_frame = CTkFrame(master=window, width=650, height=500, corner_radius=0)
    support_frame.place(x=150, y=0)

    help_label = CTkLabel(support_frame, text=translate("help_text"), font=("Noto Kufi Arabic", 15), anchor="center")
    help_label.pack(anchor="center")

    help_label1 = CTkLabel(support_frame, text=translate("help_text_2"), font=("Noto Kufi Arabic", 15))
    help_label1.pack(anchor="center")

    discord_btn = CTkButton(master=support_frame, text=translate("discord"), corner_radius=15, command=web)
    discord_btn.pack(anchor="center")

    support_btn = CTkButton(btn_frame, text=translate("support"), corner_radius=15, command=lambda: support_frame.tkraise())
    support_btn.place(x=4, y=60)
    
    # Language buttons
    lang_frame = CTkFrame(window, width=150, height=500, corner_radius=15)
    lang_frame.place(x=650, y=0)

    en_btn = CTkButton(lang_frame, text="English", corner_radius=15, command=lambda: change_language("en"))
    en_btn.pack(pady=10)

    ar_btn = CTkButton(lang_frame, text="العربية", corner_radius=15, command=lambda: change_language("ar"))
    ar_btn.pack(pady=10)
        
    lang_btn = CTkButton(btn_frame, text=translate("support"), corner_radius=15, command=lambda: lang_frame.tkraise())
    lang_btn.place(x=4, y=60)

    lang_frame.tkraise()
    window.mainloop()

if __name__ == "__main__":
    main()