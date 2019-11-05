import sys
import os
import requests,json
from frappeclient import FrappeClient
from datetime import datetime
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK,const
from tkinter import *
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
import subprocess,cmd

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

def bioconnect(bioip,attdate,attdate1):
    conn = None
    client = FrappeClient("https://erpmaxdclghana.com", "Administrator", "S3kur1tiGH")
    bioip = bioip.split(":")
    zk= ZK(bioip[1],port=4370)
    try:
        conn = zk.connect()
        curdate = datetime.now().date()
        attendance = conn.get_attendance()
        for att in attendance:
            biodate = att.timestamp.date()
            userid = att.user_id			
            if biodate >= attdate and biodate <= attdate1:		
                biotime = att.timestamp.time()
                emp = client.get_value("Employee",["name","employee_number"],
                                 {"biometric_id": userid,"status":"Active"})
                if emp:
                    fetch_attendance(client,emp["name"],biodate,biotime)
                    
    except Exception as e:
        print e
        messagebox.showinfo('Error',e)

def fetch_attendance(client,userid,biodate,biotime):
    biodate = str(biodate)
    biotime = str(biotime)
    intime = outtime = ""
    submit = False
    doj = client.get_value("Employee", ["date_of_joining"],{"employee":userid})
    if doj:
        doj = doj['date_of_joining']
        if str(doj) <= biodate:
            att = client.get_value("Attendance",["status","name","in_time","docstatus"],
                                        {"employee":userid,"attendance_date": biodate}) 
            if att:
                times = []
                doc = client.get_doc("Attendance",att["name"]) 
                if att["in_time"]:
                    times = [att["in_time"],biotime]
                    intime = min(times)
                    outtime = max(times)
                    status = "Present"
                    if intime and outtime:
                        intime_f = datetime.strptime(intime,'%H:%M:%S')
                        outtime_f = datetime.strptime(outtime,'%H:%M:%S')
                        twh = outtime_f - intime_f
                        doc["total_working_hour"] = str(twh)
                        
                    if att["docstatus"] == 0:
                        doc["docstatus"] = 1
                else:
                    intime = biotime
            else:
                doc = {"doctype":"Attendance"}
                intime = biotime		
                doc["employee"] = userid
                status = "Absent"

            
            doc["attendance_date"] = biodate
            doc["in_time"] = intime
            doc["out_time"] = outtime

            if att:
                client.update(doc)
            else:
                client.insert(doc) 
        
def clicked():
    bioconnect(var.get(),cal.get_date(),cal1.get_date())
    messagebox.showinfo('Info','Attendance Updated')
    
if __name__ == "__main__":
    window = tk.Tk()
    progress = ttk.Progressbar(window,orient=HORIZONTAL,length=200,mode='indeterminate')
    window.title("HO Biometric")
    window.geometry("300x300")
    var = tk.StringVar(window)
    var.set("HO:192.168.0.244") # initial value
    ttk.Label(window, text='Select IP').pack(padx=10, pady=10)
    option = tk.OptionMenu(window, var, "HO:192.168.0.244")
    option.pack()
    ttk.Label(window, text='Choose date').pack(padx=10, pady=10)
    cal = DateEntry(window, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2019)
    cal.pack(padx=10, pady=10)
    cal1 = DateEntry(window, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2019)
    cal1.pack(padx=10, pady=10)
    fetchBtn = ttk.Button(window, text="Fetch",command=clicked)
    fetchBtn.pack(padx=10, pady=10)

    
    window.mainloop()
