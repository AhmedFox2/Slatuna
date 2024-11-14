import requests as rq, os, json as j, datetime as dt, sys,time as t
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

# تغيير دليل العمل إلى دليل الملف الحالي
loc = os.path.dirname(__file__)
os.chdir(loc)

# تحميل ملف JSON
def load_json_file():
    while True:
        try:
            with open(f"{loc}/assets/data/database.json", "r") as thefile:
                return j.load(thefile)
        except (j.decoder.JSONDecodeError, FileNotFoundError):
            initial_data = {
                "sys": {
                    "year": "1",
                    "month": "",
                    "version": "",
                    "converted":"no",
                    "ready":"no",
                    "times": []
                }
            }
            with open(f"{loc}/assets/data/database.json", "w") as controler:
                j.dump(initial_data, controler, indent=4)

# حفظ ملف JSON
def save_json_file(data):
    with open(f"{loc}/assets/data/database.json", "w") as f:
        j.dump(data, f, indent=4)

# تحميل أوقات الصلاة
def fetch_prayer_times(city, year, month):
    url = f'https://timesprayer.com/en/list-prayer-in-{city}-{year}-{month}.html'
    response = rq.get(url)
    soup = bs(response.content, "html.parser")
    times_table = soup.find(class_="prayertimerange").find_all('td')
    return times_table

# معالجة أوقات الصلاة
def process_prayer_times(times_table):
    the_database_list = [td.text for td in times_table]
    the_date_list = the_database_list[::7]
    the_times_list = [the_database_list[i].split()[0] for i in range(len(the_database_list)) if i % 7 != 0]
    the_times_during_list = [the_database_list[i].split()[1] for i in range(len(the_database_list)) if i % 7 != 0]
    return the_date_list, the_times_list, the_times_during_list
#  تحديث ملف JSON بأوقات الصلاة
def update_json_with_prayer_times(json_data, date_list, times_list, times_during_list):
    for i in range(len(date_list)):
        daily_times = {
            "date_for": date_list[i],
            "all_times": times_list[i*6:(i+1)*6],
            "all_times_during": times_during_list[i*6:(i+1)*6],
            "all_times_2":times_list[i*6:(i+1)*6]
        }
        json_data["sys"]["times"].append(daily_times)
    save_json_file(json_data)

# التحقق من صحة التاريخ وتحديثه إذا لزم الأمر
def validate_date(json_data, current_date):
    current_month,current_day =  current_date.month,current_date.day
    
    database_date = json_data["sys"]["times"][0]["date_for"].split("-")
    database_month,database_day = int(database_date[1]), int(database_date[2])
    
    if current_month != database_month or current_day != database_day or not json_data["sys"]["times"]:
        json_data["sys"]["month"] = current_month

        while json_data["sys"]["times"] and (current_month != database_month or current_day > database_day):
            database_day = int(json_data["sys"]["times"][0]["date_for"].split("-")[2])     
            if database_month != current_month or database_day < current_day:
                json_data["sys"]["times"].pop(0)
            else:
                break

        save_json_file(json_data)
    else:
        None

#تحويل الاوقات من 12 ساعه الي 24 ساعه
def convert_the_time_to_24h():
    fileopend = load_json_file()
    
    the_convertor = {"1":"13","2":"14","3":"15","4":"16","5":"17","6":"18","7":"19","8":"20","9":"21","10":"22","11":"23","12":"12"}
    all_pray = fileopend["sys"]["times"]
    
    if fileopend["sys"]["converted"] == "no":
        for i in range(len(all_pray)):
            try:
                the_frist_one_time = fileopend["sys"]["times"][i]["all_times"]
                the_frist_one_during = fileopend["sys"]["times"][i]["all_times_during"]

                the_new_list =[]
                for (time,during) in zip(the_frist_one_time,the_frist_one_during):
                    if during == "PM":
                        the_time = str(time).split(":")
                        the_24_time = the_convertor[the_time[0]]

                        the_new_one = f"{the_24_time}:{the_time[1]}"
                        the_new_list.append(the_new_one)

                        fileopend["sys"]["times"][i]["all_times"] = the_new_list
                    else:
                        the_new_list.append(time)
            except KeyError:
                pass
    else:
        None
    fileopend["sys"]["converted"] = "yes"
    save_json_file(fileopend)

#انشاء نسخه اخري من اوقات الصلاه
def duplicat():
    fileopend = load_json_file()
    
    all_pray = fileopend["sys"]["times"]

    if fileopend["sys"]["ready"] == "no":
        for i in range(len(all_pray)):

            the_frist_one = fileopend["sys"]["times"][i]["all_times"]
            fileopend["sys"]["times"][i]["all_times_2"] = the_frist_one
            fileopend["sys"]["ready"] = "yes"
            save_json_file(fileopend)
    else:
        None

#التاكد من صحة الاوقات اذن كانت فائته ام لا
def check_the_pray_times():
    fileopend = load_json_file()

    current_time_str = t.strftime("%H:%M")
    current_time = get_time_in_minutes(current_time_str)

    current_date = dt.datetime.now().date()
    current_day = current_date.day
    
    remaining_prayer_times = []
    remaining_all_times = []

    all_pray = fileopend["sys"]["times"][0]["all_times"]
    all_times = fileopend["sys"]["times"][0]["all_times_during"]
    prayer_times = [get_time_in_minutes(pray) for pray in all_pray]

    the_datebase_day = str(fileopend["sys"]["times"][0]["date_for"]).split("-")[2]

    for i,(pray,time) in enumerate(zip(prayer_times,all_times)):
        if  str(current_day) < the_datebase_day:
            break
        elif current_time < pray:
            remaining_prayer_times.append(all_pray[i])
            remaining_all_times.append(time)

        fileopend["sys"]["times"][0]["all_times"] = remaining_prayer_times
        fileopend["sys"]["times"][0]["all_times_during"] = remaining_all_times
    save_json_file(fileopend)

# الوظيفة الرئيسية
def main():
    json_data = load_json_file()
    current_date = dt.datetime.now().date()
    current_year, current_month, current_day = current_date.year, current_date.month, current_date.day

    json_year = json_data["sys"]["year"]

    if current_year != json_year or not json_data["sys"]["times"]:
        print("Year mismatch found or no times available. Fetching new prayer times.")
        response = urlopen('http://ipinfo.io/json')
        data = j.load(response)
        city = data["city"]
        print(f"Detected city: {city}")

        version = bs(rq.get("https://ahmedfox2.github.io/Slatuna.github.io/").content, "html.parser").find("h1").text
        print(f"Detected version: {version}")

        json_data["sys"].update({
            "year": current_year,
            "month": current_month,
            "version": version
        })

        for month in range(current_month, 13):
            print(f"Fetching prayer times for month: {month}")
            times_table = fetch_prayer_times(city, current_year, month)
            date_list, times_list, times_during_list = process_prayer_times(times_table)
            update_json_with_prayer_times(json_data, date_list, times_list, times_during_list)
    validate_date(json_data, current_date)
    convert_the_time_to_24h()
    duplicat()
    check_the_pray_times()
    print("Data validation complete and updated if necessary")

#دالة مساعدة في تحويل الوقت الي date time
def get_time_in_minutes(time_str):
    time_obj = dt.datetime.strptime(time_str, "%H:%M").time()
    return dt.timedelta(hours=time_obj.hour, minutes=time_obj.minute)

# استدعاء الدالة الرئيسية
if __name__ == "__main__":
    main()