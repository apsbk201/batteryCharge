#!/usr/bin/python3
import tkinter as tk
import psutil
import time
import platform
import os
# Check OS
global os_windows
os_windows = False
if platform.system() == "Windows":
    import winsound
    os_windows = True

def sound():
    if os_windows:
        duration = 1000 # ms
        freq = 3000 # Hz
        winsound.Beep(freq, duration)
        #time.sleep(0.1)
        #winsound.Beep(freq, duration)
    else:
        duration = 0.4 # secouds
        freq =4440 # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
        time.sleep(0.1)
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

# function returning time in hh:mm:ss
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def readBatt():
    battery = psutil.sensors_battery()
    batt_percent = float("%.2f" % battery.percent)
#    print(type(batt_percent))
    time_left = convertTime(battery.secsleft)
    plugin = battery.power_plugged
    # print("Battery percent : ","%.2f" % battery.percent)
    # print("Battery left : ", convertTime(battery.secsleft))
    # print("Power Plugin : ",battery.power_plugged)
    return batt_percent, time_left, plugin
#print(readBatt())

def appnotify(batt_percent, time_left):
    global app
    click = False
    sound()
    app = tk.Tk()
    app.geometry("240x120")
    app.title("Please Charge")

    frame1 = tk.Frame()
    frame2 = tk.Frame()
    frame3 = tk.Frame()
    percent = "Battery percent : " + str(batt_percent) + " %"
    battery_left = "Time left : " + time_left

    label1 = tk.Label(master=frame1, text='Baterry Low !!', bg='yellow', fg='red').pack()
    label2 = tk.Label(master=frame2, text=percent, fg='red').pack()
    label3 = tk.Label(master=frame3, text=battery_left).pack()

    button = tk.Button(text='(--- OK ---)',fg='blue', command=lambda : clicked())

    frame1.pack()
    frame2.pack()
    frame3.pack()
    button.pack()

    app.mainloop()

def clicked():
    # exit()
    app.destroy()

#old_percent = int(readBatt()[0])
old_percent = 90

while True:
    try :
        new_percent = int(readBatt()[0])
        print(f"New {new_percent}  Old {old_percent}")
        if new_percent >= 40 and new_percent <= 43 :
            print(f"readbbatt[2] {not readBatt()[2]} ")
            if not readBatt()[2] and new_percent != old_percent :
                old_percent = int(readBatt()[0])
                appnotify(new_percent, str(readBatt()[1]))
                # print(f"new = {new_percent}  time = {readBatt()[1]}")
                time.sleep(30)
        if new_percent >= 5 and new_percent <= 24 :
            if not readBatt()[2] and new_percent != old_percent :
                old_percent = int(readBatt()[0])
                appnotify(new_percent, str(readBatt()[1]))

        time.sleep(30)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
